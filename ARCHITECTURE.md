# ARCHITECTURE.md — Архитектура системы

## Назначение файла
Этот файл описывает архитектуру проекта для понимания системы
и служит справочником при разработке каждого компонента.

---

## Общая схема взаимодействия

```
Пользователь
    │
    ├─── [Браузер / Swagger] ──────► Auth Service (FastAPI :8000)
    │                                    │
    │                               ┌────┴──────┐
    │                               │  SQLite/  │
    │                               │ PostgreSQL│
    │                               └───────────┘
    │
    └─── [Telegram] ──────────────► Bot Service (aiogram)
                                        │
                              ┌─────────┼──────────┐
                              │         │          │
                           Redis    RabbitMQ    Validate JWT
                         (хранение  (broker)   (без обращения
                          токенов)              к Auth Service)
                                         │
                                    Celery Worker
                                         │
                                    OpenRouter API
                                    (LLM ответ)
```

## Сервис 1: Auth Service

### Назначение
Единственная точка управления пользователями и выдачи JWT-токенов.

### Endpoints
| Метод | Путь           | Описание                          |
|-------|----------------|-----------------------------------|
| POST  | /auth/register | Регистрация нового пользователя   |
| POST  | /auth/login    | Логин, возвращает JWT             |
| GET   | /auth/me       | Профиль пользователя по JWT       |
| GET   | /health        | Health-check сервиса              |

### Структура JWT payload
```json
{
  "sub": "user_id (UUID)",
  "role": "user | admin",
  "iat": 1700000000,
  "exp": 1700003600
}
```

### Стек слоёв
```
routes_auth.py (HTTP layer)
    ↓
auth.py (usecases — бизнес-логика)
    ↓
users.py (repository — только SQL)
    ↓
SQLAlchemy async session → SQLite/PostgreSQL
```

---

## Сервис 2: Bot Service

### Назначение
Telegram-бот с LLM-консультациями. Не знает ничего о регистрации/логине.
Доверяет только валидному JWT.

### Пользовательский сценарий
1. Пользователь получает JWT в Swagger Auth Service
2. Отправляет боту команду `/token <jwt>`
3. Бот сохраняет JWT в Redis: ключ `token:<telegram_user_id>`
4. Пользователь пишет текстовое сообщение
5. Бот читает JWT из Redis → валидирует подпись и exp
6. Публикует задачу в RabbitMQ через Celery: `llm_request.delay(chat_id, text)`
7. Celery Worker забирает задачу, вызывает OpenRouter API
8. Ответ LLM отправляется пользователю в Telegram

### Компоненты Bot Service
```
handlers.py         ← приём сообщений Telegram
    ↓
get_redis()         ← чтение/запись JWT в Redis
    ↓
decode_and_validate() ← проверка JWT (app/core/jwt.py)
    ↓
llm_request.delay() ← публикация в RabbitMQ
    ↓
Celery Worker
    ↓
openrouter_client.py ← вызов LLM API
    ↓
Telegram (ответ пользователю)
```

---

## Инфраструктура (Docker Compose)

| Сервис         | Образ                  | Порт    | Назначение                      |
|----------------|------------------------|---------|----------------------------------|
| auth_service   | python:3.11-slim       | 8000    | FastAPI Auth Service             |
| bot_service    | python:3.11-slim       | 8001    | FastAPI health + bot runner      |
| celery_worker  | python:3.11-slim       | —       | Celery Worker для LLM задач      |
| rabbitmq       | rabbitmq:3-management  | 5672    | Broker задач Celery              |
|                |                        | 15672   | RabbitMQ Management UI           |
| redis          | redis:7-alpine         | 6379    | Cache + Celery result backend    |

---

## Безопасность

- Пароли хранятся ТОЛЬКО в виде bcrypt-хеша
- JWT подписывается HS256 с секретом из env-переменной
- Bot Service не имеет доступа к БД Auth Service
- JWT_SECRET должен совпадать в обоих .env файлах
- Токены имеют ограниченный срок действия (ACCESS_TOKEN_EXPIRE_MINUTES)

---

## Тестирование

### Auth Service тесты
- `tests/test_security.py` — unit тесты хеширования и JWT
- `tests/test_auth_integration.py` — интеграционные HTTP тесты

### Bot Service тесты
- `tests/test_jwt.py` — unit тесты валидации JWT
- `tests/test_handlers.py` — мок-тесты Telegram handlers
- `tests/test_openrouter.py` — интеграционные тесты (respx mock)
