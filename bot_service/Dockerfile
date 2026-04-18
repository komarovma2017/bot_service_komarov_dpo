# Dockerfile для Bot Service
# Один образ используется и для FastAPI health-check, и для Celery worker,
# и для запуска aiogram бота — команда задаётся через docker-compose
FROM python:3.11-slim

WORKDIR /app

# Установить uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml ./

RUN uv sync --no-dev

COPY . .

EXPOSE 8001

# По умолчанию запускаем FastAPI health-check
# Celery worker и бот запускаются отдельными командами в docker-compose
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
