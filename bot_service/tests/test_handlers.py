# Мок-тесты Telegram-обработчиков с fakeredis

from unittest.mock import AsyncMock, MagicMock, patch

import fakeredis.aioredis
import pytest
from aiogram.types import Chat, Message, User
from jose import jwt

from app.core.config import settings
import app.bot.handlers as handlers_mod


def _make_token(sub: str = "user-1", role: str = "user") -> str:
    payload = {"sub": sub, "role": role}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


@pytest.fixture
def fake_redis():
    """Создаёт fakeredis-клиент."""
    return fakeredis.aioredis.FakeRedis(decode_responses=True)


@pytest.fixture
def mock_message():
    """Создаёт фейковое Telegram-сообщение."""
    msg = MagicMock(spec=Message)
    msg.from_user = MagicMock(spec=User)
    msg.from_user.id = 12345
    msg.chat = MagicMock(spec=Chat)
    msg.chat.id = 12345
    msg.answer = AsyncMock()
    return msg


@pytest.mark.asyncio
async def test_token_command_saves_to_redis(fake_redis, mock_message):
    """Команда /token сохраняет токен в Redis под ключом token:<user_id>."""
    token = _make_token()
    mock_message.text = f"/token {token}"

    with patch.object(handlers_mod, "get_redis", return_value=fake_redis):
        await handlers_mod.cmd_token(mock_message)

    stored = await fake_redis.get("token:12345")
    assert stored == token


@pytest.mark.asyncio
async def test_text_without_token(fake_redis, mock_message):
    """Без токена Celery НЕ вызывается, бот отвечает об ошибке."""
    mock_message.text = "Привет!"

    with patch.object(handlers_mod, "get_redis", return_value=fake_redis):
        await handlers_mod.handle_text(mock_message)

    mock_message.answer.assert_called_once()
    assert "не авторизованы" in mock_message.answer.call_args[0][0]


@pytest.mark.asyncio
async def test_text_with_token_calls_celery(fake_redis, mock_message):
    """С токеном llm_request.delay вызывается с правильными аргументами."""
    token = _make_token()
    await fake_redis.set("token:12345", token)
    mock_message.text = "Расскажи про Python"

    with patch.object(handlers_mod, "get_redis", return_value=fake_redis), \
         patch.object(handlers_mod, "llm_request") as mock_llm:
        mock_llm.delay = MagicMock()
        await handlers_mod.handle_text(mock_message)

    mock_llm.delay.assert_called_once_with(12345, "Расскажи про Python")
    mock_message.answer.assert_called_once()
    assert "Запрос принят" in mock_message.answer.call_args[0][0]
