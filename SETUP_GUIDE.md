# SETUP_GUIDE.md — Инструкция настройки рабочего места
# Операционная система: РЕД ОС 8 (REDOS 8)
#
# РЕД ОС 8 основана на RHEL 8 / Fedora.
# Менеджер пакетов: dnf (НЕ apt!)
# Формат пакетов: RPM (НЕ deb!)
# Этот файл НЕ коммитится в финальный вид проекта.

---

## Шаг 1: Обновить систему

```bash
# Обновить все установленные пакеты
sudo dnf update -y

# Установить базовые утилиты (curl, wget, git, unzip)
sudo dnf install -y curl wget git unzip bash-completion
```

---

## Шаг 2: Установить Python 3.11+

РЕД ОС 8 поставляется с Python 3.9 по умолчанию.
Python 3.11 устанавливается через dnf из стандартного репозитория.

```bash
# Установить Python 3.11 и инструменты разработчика
sudo dnf install -y python3.11 python3.11-devel

# Проверить версию
python3.11 --version

# Установить pip для python3.11 (если нужен)
python3.11 -m ensurepip --upgrade
```

---

## Шаг 3: Установить uv (менеджер пакетов Python)

uv — современный и быстрый менеджер пакетов Python, заменяет pip и venv.

```bash
# Установка uv через официальный скрипт
curl -LsSf https://astral.sh/uv/install.sh | sh

# Перезагрузить переменные окружения
source $HOME/.local/bin/env
# или добавить в ~/.bashrc и перезапустить терминал:
echo 'source $HOME/.local/bin/env' >> ~/.bashrc
source ~/.bashrc

# Проверить установку
uv --version
```

---

## Шаг 4: Установить Node.js 20+ (нужен для Claude Code CLI)

В РЕД ОС 8 Node.js доступен через dnf, но версия может быть старой.
Рекомендуется использовать NVM для установки актуальной версии.

### Вариант А: через dnf (проще, но версия может быть не 20+)
```bash
# Установить Node.js из репозитория РЕД ОС
sudo dnf install -y nodejs npm

# Проверить версию
node --version
npm --version
```

### Вариант Б: через NVM (рекомендуется — даёт Node.js 20+)
```bash
# Установить NVM (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Перезагрузить переменные окружения
source ~/.bashrc

# Установить Node.js версии 20 (LTS)
nvm install 20
nvm use 20
nvm alias default 20

# Проверить версии
node --version   # должно быть v20+
npm --version
```

---

## Шаг 5: Установить Docker и docker-compose

В РЕД ОС 8 Docker устанавливается через dnf из репозитория РЕД СОФТ.

```bash
# Установить Docker CE и CLI
sudo dnf install -y docker-ce docker-ce-cli

# Запустить Docker и добавить в автозагрузку
sudo systemctl enable docker --now

# Проверить статус
sudo systemctl status docker

# Добавить текущего пользователя в группу docker
# (чтобы не писать sudo перед каждой docker командой)
sudo usermod -aG docker $USER

# ВАЖНО: выйти из сессии и зайти снова, чтобы изменения группы вступили в силу
# newgrp docker   # или перелогиниться

# Установить docker-compose
sudo dnf install -y docker-compose

# Проверить версии
docker --version
docker-compose --version
# или для нового формата:
docker compose version
```

### Если docker-ce нет в репозитории РЕД ОС:
```bash
# Добавить официальный репозиторий Docker (для RHEL-совместимых систем)
sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo

# После этого установить Docker
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

sudo systemctl enable docker --now
sudo usermod -aG docker $USER
```

---

## Шаг 6: Установить Claude Code CLI

```bash
# Установить Claude Code глобально через npm
npm install -g @anthropic-ai/claude-code

# Проверить установку
claude --version
```

---

## Шаг 7: Подключить GLM 5.1 через OpenRouter к Claude Code

Claude Code по умолчанию работает с моделями Anthropic.
Для использования GLM 5.1 (через OpenRouter) задаём переменные окружения.

```bash
# Добавить в ~/.bashrc (чтобы работало при каждом входе)
cat >> ~/.bashrc << 'ENV_EOF'

# Claude Code CLI — подключение к OpenRouter (GLM 5.1)
export ANTHROPIC_BASE_URL=https://openrouter.ai/api/v1
export ANTHROPIC_API_KEY=ваш_ключ_openrouter_здесь
ENV_EOF

# Применить изменения
source ~/.bashrc

# Проверить что переменные установлены
echo $ANTHROPIC_BASE_URL
echo $ANTHROPIC_API_KEY
```

**Получить ключ OpenRouter:** https://openrouter.ai/keys

При запуске Claude Code можно явно указать модель:
```bash
# Запустить Claude Code с моделью GLM 5.1
claude --model glm-z1-flash:free

# Или указать модель в настройках проекта (CLAUDE.md уже содержит инструкции)
```

---

## Шаг 8: Клонировать репозиторий

```bash
# Перейти в домашнюю директорию пользователя
cd ~

# Клонировать пустой репозиторий GitHub
git clone https://github.com/komarovma2017/bot_service_komarov_dpo

# Перейти в директорию
cd bot_service_komarov_dpo

# Убедиться что git настроен
git config --global user.name "Ваше Имя"
git config --global user.email "komarov@email.com"
```

---

## Шаг 9: Распаковать набор файлов в репозиторий

```bash
# Скопировать ZIP-архив из Windows на РЕД ОС:
# - через USB-носитель
# - через scp: scp bot_service_komarov_dpo_setup.zip user@redos-host:~/
# - через общую папку

# Распаковать архив поверх клонированного репозитория
cd ~/bot_service_komarov_dpo
python3.11 -c "
import zipfile, os
with zipfile.ZipFile('../bot_service_komarov_dpo_setup.zip') as z:
    for member in z.namelist():
        # Убрать первый уровень директории из пути
        parts = member.split('/', 1)
        if len(parts) > 1 and parts[1]:
            target = parts[1]
            if member.endswith('/'):
                os.makedirs(target, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(target) or '.', exist_ok=True)
                with z.open(member) as src, open(target, 'wb') as dst:
                    dst.write(src.read())
                    print(f'  извлечён: {target}')
"

# Проверить что файлы на месте
ls -la
```

---

## Шаг 10: Настроить .env файлы

```bash
cd ~/bot_service_komarov_dpo

# Создать .env из шаблонов
cp auth_service/.env.example auth_service/.env
cp bot_service/.env.example bot_service/.env

# Заполнить секреты (открыть в редакторе)
nano auth_service/.env
# Изменить: JWT_SECRET=ваш_секрет_минимум_32_символа

nano bot_service/.env
# Изменить:
#   TELEGRAM_BOT_TOKEN=токен_от_BotFather
#   JWT_SECRET=тот_же_секрет_что_в_auth_service
#   OPENROUTER_API_KEY=ваш_ключ_openrouter
```

---

## Шаг 11: Запустить Claude Code CLI в проекте

```bash
# Перейти в директорию проекта
cd ~/bot_service_komarov_dpo

# Запустить Claude Code
claude

# Claude Code автоматически прочитает CLAUDE.md и RULES.md
# Открой TASKS.md и выдавай задачи по одному шагу
```

---

## Полезные команды во время разработки

```bash
# Запустить всю инфраструктуру
docker-compose up --build

# Только инфраструктура (Redis + RabbitMQ), без сервисов
docker-compose up rabbitmq redis -d

# Логи конкретного сервиса
docker-compose logs auth_service -f

# Остановить всё
docker-compose down

# Остановить и удалить данные (сброс БД и очередей)
docker-compose down -v

# Запустить тесты Auth Service
cd auth_service && uv run pytest tests/ -v

# Запустить тесты Bot Service
cd ../bot_service && uv run pytest tests/ -v
```

---

## Устранение возможных проблем на РЕД ОС 8

### Проблема: SELinux блокирует Docker
```bash
# Проверить статус SELinux
getenforce

# Временно отключить (для разработки)
sudo setenforce 0

# Или настроить политику для Docker
sudo setsebool -P container_manage_cgroup true
```

### Проблема: Firewall блокирует порты
```bash
# Открыть порты для разработки
sudo firewall-cmd --permanent --add-port=8000/tcp   # Auth Service
sudo firewall-cmd --permanent --add-port=8001/tcp   # Bot Service
sudo firewall-cmd --permanent --add-port=15672/tcp  # RabbitMQ UI
sudo firewall-cmd --permanent --add-port=5672/tcp   # RabbitMQ AMQP
sudo firewall-cmd --permanent --add-port=6379/tcp   # Redis
sudo firewall-cmd --reload
```

### Проблема: python3.11 не найден
```bash
# Проверить доступные версии Python
dnf list available | grep python3

# Установить через alternatives если нужно несколько версий
sudo alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

---

## Важно: что НЕ коммитить на GitHub
- Файлы `.env` (содержат секреты токены и пароли!)
- Файлы `*.db` (база данных SQLite)
- Директории `.venv/` (виртуальные окружения Python)
- `__pycache__/` (скомпилированный Python)
- Этот файл можно удалить перед финальным push: `rm SETUP_GUIDE.md`

Все исключения уже прописаны в `.gitignore`.
