# CLAUDE.md — Инструкции для Claude Code CLI

## О проекте
Это учебный итоговый проект: **Двухсервисная система LLM-консультаций**.
Разрабатываем распределённую систему из двух микросервисов:
- **Auth Service** (FastAPI, порт 8000) — регистрация, логин, выдача JWT
- **Bot Service** (aiogram + Celery, порт 8001) — Telegram-бот с LLM через OpenRouter

## Стек технологий
- Python 3.11+, менеджер пакетов: `uv`
- FastAPI + SQLAlchemy (async) + aiosqlite
- aiogram 3.x для Telegram-бота
- Celery + RabbitMQ (broker) + Redis (backend/cache)
- OpenRouter API для LLM (модель: stepfun/step-3.5-flash:free)
- Docker + docker-compose для оркестрации
- pytest + pytest-asyncio + fakeredis + respx для тестов

## Структура репозитория
```
bot_service_komarov_dpo/
├── auth_service/          # Сервис аутентификации
│   ├── app/
│   │   ├── main.py
│   │   ├── core/          # config, security, exceptions
│   │   ├── db/            # base, session, models
│   │   ├── schemas/       # pydantic схемы
│   │   ├── repositories/  # слой доступа к БД
│   │   ├── usecases/      # бизнес-логика
│   │   └── api/           # роуты, deps, router
│   ├── tests/
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── .env
├── bot_service/           # Сервис Telegram-бота
│   ├── app/
│   │   ├── main.py
│   │   ├── core/          # config, jwt
│   │   ├── infra/         # redis, celery_app
│   │   ├── tasks/         # llm_tasks (Celery)
│   │   ├── services/      # openrouter_client
│   │   └── bot/           # dispatcher, handlers
│   ├── tests/
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── .env
├── docker-compose.yml
├── CLAUDE.md              # этот файл
├── RULES.md               # правила разработки
├── ARCHITECTURE.md        # архитектурная документация
└── README.md              # финальная документация проекта
```

## Принципы архитектуры (ОБЯЗАТЕЛЬНО соблюдать!)
1. **Auth Service** — только регистрация, логин, выдача JWT. Никакой логики бота.
2. **Bot Service** — только валидация JWT (не создаёт токены!), приём сообщений, публикация в очередь.
3. **Разделение ответственности**: репозиторий → юзкейс → роут (никогда не смешивать слои).
4. **JWT_SECRET** должен быть одинаковым в обоих сервисах (через .env).
5. LLM-запросы ТОЛЬКО через Celery (не в хэндлерах напрямую!).
6. Redis хранит JWT привязанный к Telegram user_id по ключу `token:<tg_user_id>`.

## Команды разработки

### Запуск сервисов через docker-compose
```bash
docker-compose up --build
```

### Запуск Auth Service локально
```bash
cd auth_service
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Запуск Bot Service локально
```bash
cd bot_service
uv run python -m app.main          # FastAPI health-check
uv run celery -A app.infra.celery_app worker --loglevel=info  # Celery worker
uv run python -m app.bot.dispatcher  # aiogram бот
```

### Запуск тестов
```bash
cd auth_service && uv run pytest tests/ -v
cd bot_service  && uv run pytest tests/ -v
```

## Важные замечания для Claude
- Не добавляй упоминания Claude/Anthropic в код или комментарии
- Все комментарии в коде пиши на русском языке (для учебной цели)
- Следуй точной структуре файлов из task.txt
- Используй `uv` а не `pip` для управления зависимостями
- В docker-compose используй имена сервисов `rabbitmq` и `redis` (не localhost)
