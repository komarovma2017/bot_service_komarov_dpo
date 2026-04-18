# Celery-задача: LLM-запрос через OpenRouter

import asyncio
import logging

from aiogram import Bot

from app.core.config import settings
from app.infra.celery_app import celery_app
from app.services.openrouter_client import call_openrouter

logger = logging.getLogger(__name__)


@celery_app.task(name="llm_request")
def llm_request(tg_chat_id: int, prompt: str) -> None:
    """Задача: вызывает OpenRouter и отправляет ответ в Telegram."""
    try:
        answer = asyncio.run(call_openrouter(prompt))
    except Exception as e:
        logger.error("Ошибка OpenRouter: %s", e)
        answer = "Произошла ошибка при обращении к LLM. Попробуйте позже."

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    try:
        asyncio.run(bot.send_message(chat_id=tg_chat_id, text=answer))
    except Exception as e:
        logger.error("Ошибка отправки в Telegram: %s", e)
    finally:
        asyncio.run(bot.session.close())
