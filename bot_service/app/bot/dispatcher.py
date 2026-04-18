# Сборка aiogram Bot + Dispatcher

import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.bot.handlers import router as handlers_router
from app.core.config import settings

logger = logging.getLogger(__name__)

dp = Dispatcher()
dp.include_router(handlers_router)

# Глобальный экземпляр бота
_bot: Bot | None = None


def get_bot() -> Bot:
    global _bot
    if _bot is None:
        _bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    return _bot


async def main():
    """Запуск long-polling бота."""
    bot = get_bot()
    logger.info("Запуск Telegram-бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
