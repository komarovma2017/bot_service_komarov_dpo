# TASKS.md — Пошаговый план разработки

## Как использовать этот файл
Перед запуском Claude Code CLI открой этот файл.
Выдавай Claude Code задачи по одному шагу.
Отмечай выполненные задачи символом ✅

---

## ФАЗА 1: Auth Service — основа

### Шаг 1.1 — Конфигурация и исключения
Задача для Claude Code:
> "Создай файлы auth_service/app/core/config.py и auth_service/app/core/exceptions.py
> согласно RULES.md и ARCHITECTURE.md. Используй pydantic-settings.
> Исключения: UserAlreadyExistsError, InvalidCredentialsError, InvalidTokenError,
> TokenExpiredError, UserNotFoundError, PermissionDeniedError"

- [ ] auth_service/app/core/config.py
- [ ] auth_service/app/core/exceptions.py

### Шаг 1.2 — Безопасность (bcrypt + JWT)
Задача для Claude Code:
> "Создай auth_service/app/core/security.py с функциями:
> hash_password(), verify_password(), create_access_token(), decode_token().
> JWT должен содержать поля sub, role, iat, exp. Используй python-jose."

- [ ] auth_service/app/core/security.py

### Шаг 1.3 — База данных
Задача для Claude Code:
> "Создай три файла БД для Auth Service:
> app/db/base.py (Base = DeclarativeBase()),
> app/db/session.py (async engine + AsyncSessionLocal),
> app/db/models.py (модель User с полями id, email, password_hash, role, created_at).
> Обязательно: уникальный индекс на email."

- [ ] auth_service/app/db/base.py
- [ ] auth_service/app/db/session.py
- [ ] auth_service/app/db/models.py

### Шаг 1.4 — Схемы Pydantic
Задача для Claude Code:
> "Создай auth_service/app/schemas/auth.py (RegisterRequest, TokenResponse)
> и auth_service/app/schemas/user.py (UserPublic с id, email, role, created_at).
> В UserPublic НИКОГДА не должно быть password_hash."

- [ ] auth_service/app/schemas/auth.py
- [ ] auth_service/app/schemas/user.py

### Шаг 1.5 — Репозиторий
Задача для Claude Code:
> "Создай auth_service/app/repositories/users.py с методами:
> get_by_id(), get_by_email(), create().
> Репозиторий не бросает HTTPException, только возвращает данные или None."

- [ ] auth_service/app/repositories/users.py

### Шаг 1.6 — Бизнес-логика (usecases)
Задача для Claude Code:
> "Создай auth_service/app/usecases/auth.py с методами register(), login(), me().
> Используй только исключения из app/core/exceptions.py (не HTTPException напрямую).
> Не пиши SQL — только вызовы репозитория."

- [ ] auth_service/app/usecases/auth.py

### Шаг 1.7 — API слой
Задача для Claude Code:
> "Создай auth_service/app/api/deps.py (get_db, get_users_repo, get_auth_uc, get_current_user),
> auth_service/app/api/routes_auth.py (эндпоинты /auth/register, /auth/login, /auth/me),
> auth_service/app/api/router.py (сборка роутеров),
> auth_service/app/main.py (создание FastAPI приложения)."

- [ ] auth_service/app/api/deps.py
- [ ] auth_service/app/api/routes_auth.py
- [ ] auth_service/app/api/router.py
- [ ] auth_service/app/main.py

---

## ФАЗА 2: Auth Service — тесты

### Шаг 2.1 — Unit тесты
Задача для Claude Code:
> "Создай auth_service/tests/test_security.py с тестами:
> хеширование паролей, verify_password (правильный/неправильный пароль),
> create_access_token + decode_token (проверить поля sub, role, iat, exp)."

- [ ] auth_service/tests/test_security.py

### Шаг 2.2 — Интеграционные тесты
Задача для Claude Code:
> "Создай auth_service/tests/test_auth_integration.py.
> Используй httpx ASGITransport и in-memory SQLite.
> Тесты: регистрация → логин → /auth/me, повторная регистрация (409),
> неверный пароль (401), /auth/me без токена (401)."

- [ ] auth_service/tests/test_auth_integration.py
- [ ] auth_service/tests/conftest.py

---

## ФАЗА 3: Bot Service — основа

### Шаг 3.1 — Конфигурация и JWT валидация
Задача для Claude Code:
> "Создай bot_service/app/core/config.py (BOT_TOKEN, JWT_SECRET, REDIS_URL, RABBITMQ_URL, OpenRouter настройки)
> и bot_service/app/core/jwt.py с методом decode_and_validate(token) -> dict.
> Если токен неверный или истёк — бросать ValueError."

- [ ] bot_service/app/core/config.py
- [ ] bot_service/app/core/jwt.py

### Шаг 3.2 — Инфраструктура (Redis + Celery)
Задача для Claude Code:
> "Создай bot_service/app/infra/redis.py (функция get_redis())
> и bot_service/app/infra/celery_app.py (celery_app с broker=RABBITMQ_URL, backend=REDIS_URL).
> В celery_app обязательно autodiscover_tasks или явный импорт задач."

- [ ] bot_service/app/infra/redis.py
- [ ] bot_service/app/infra/celery_app.py

### Шаг 3.3 — Celery задача LLM
Задача для Claude Code:
> "Создай bot_service/app/tasks/llm_tasks.py с задачей llm_request(tg_chat_id, prompt).
> Задача вызывает openrouter_client, получает ответ LLM и отправляет пользователю через Telegram Bot API."

- [ ] bot_service/app/tasks/llm_tasks.py

### Шаг 3.4 — OpenRouter клиент
Задача для Claude Code:
> "Создай bot_service/app/services/openrouter_client.py.
> Используй httpx для POST /chat/completions на OpenRouter.
> Обязательно обрабатывай ошибки сети и не-200 ответы."

- [ ] bot_service/app/services/openrouter_client.py

### Шаг 3.5 — Telegram Bot (dispatcher + handlers)
Задача для Claude Code:
> "Создай bot_service/app/bot/dispatcher.py (Bot + Dispatcher, регистрация хэндлеров)
> и bot_service/app/bot/handlers.py с обработчиками:
> /token <jwt> — сохранить в Redis под ключом token:<user_id>,
> обычный текст — проверить токен → llm_request.delay() → 'Запрос принят'."

- [ ] bot_service/app/bot/dispatcher.py
- [ ] bot_service/app/bot/handlers.py

### Шаг 3.6 — Точка входа Bot Service
Задача для Claude Code:
> "Создай bot_service/app/main.py — FastAPI приложение с /health эндпоинтом."

- [ ] bot_service/app/main.py

---

## ФАЗА 4: Bot Service — тесты

### Шаг 4.1 — Unit тесты JWT
Задача для Claude Code:
> "Создай bot_service/tests/test_jwt.py.
> Тест 1: корректный токен декодируется и содержит sub.
> Тест 2: мусорная строка вызывает ValueError."

- [ ] bot_service/tests/test_jwt.py

### Шаг 4.2 — Мок-тесты handlers
Задача для Claude Code:
> "Создай bot_service/tests/test_handlers.py с fakeredis.
> Тест /token: токен сохраняется в fakeredis под token:<user_id>.
> Тест без токена: Celery НЕ вызывается, бот отвечает об ошибке.
> Тест с токеном: llm_request.delay вызывается с правильными аргументами."

- [ ] bot_service/tests/test_handlers.py
- [ ] bot_service/tests/conftest.py

### Шаг 4.3 — Интеграционные тесты OpenRouter
Задача для Claude Code:
> "Создай bot_service/tests/test_openrouter.py с respx.
> Замокируй POST https://openrouter.ai/api/v1/chat/completions.
> Проверь что функция call_openrouter возвращает текст из choices[0].message.content."

- [ ] bot_service/tests/test_openrouter.py

---

## ФАЗА 5: Docker и финал

### Шаг 5.1 — Docker Compose
Задача для Claude Code:
> "Создай docker-compose.yml с сервисами: auth_service, bot_service, celery_worker,
> rabbitmq (с management UI), redis. Добавь healthcheck для каждого сервиса."

- [ ] docker-compose.yml
- [ ] auth_service/Dockerfile
- [ ] bot_service/Dockerfile

### Шаг 5.2 — README
Задача для Claude Code:
> "Создай README.md с описанием архитектуры, инструкцией запуска,
> описанием сценария работы. Добавь разделы для скриншотов."

- [ ] README.md

---

## Заметки к задачам
- После каждого шага запускай тесты: `uv run pytest tests/ -v`
- После ФАЗЫ 1-2 проверь Swagger: http://localhost:8000/docs
- После ФАЗЫ 3-4 проверь бота в Telegram
- После ФАЗЫ 5 проверь RabbitMQ UI: http://localhost:15672
