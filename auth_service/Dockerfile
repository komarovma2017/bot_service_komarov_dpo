# Dockerfile для Auth Service
# Базовый образ Python 3.11 slim (минимальный размер)
FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Установить uv — быстрый менеджер пакетов Python
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Скопировать файлы зависимостей
COPY pyproject.toml ./

# Установить зависимости (без dev зависимостей)
RUN uv sync --no-dev

# Скопировать весь код приложения
COPY . .

# Открыть порт 8000 (FastAPI)
EXPOSE 8000

# Команда запуска Auth Service
# --host 0.0.0.0 — слушать на всех интерфейсах (нужно для Docker)
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
