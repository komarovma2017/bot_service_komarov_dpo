# Обработчики Telegram: /token и обычный текст

from aiogram import Router, types
from aiogram.filters import CommandStart, Command

from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я LLM-консультант.\n"
        "Для начала отправь команду: /token <JWT>\n"
        "Получить токен можно в Swagger Auth Service."
    )


@router.message(Command("token"))
async def cmd_token(message: types.Message):
    """Сохраняет JWT в Redis под ключом token:<user_id>."""
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Использование: /token <JWT>")
        return

    token = parts[1].strip()

    try:
        payload = decode_and_validate(token)
    except ValueError:
        await message.answer("Токен недействителен. Получите новый в Auth Service.")
        return

    redis = await get_redis()
    key = f"token:{message.from_user.id}"
    await redis.set(key, token)

    await message.answer(f"Токен принят! Вы вошли как {payload.get('sub', 'пользователь')}.")


@router.message()
async def handle_text(message: types.Message):
    """Обрабатывает текстовое сообщение: проверяет токен → отправляет задачу в Celery."""
    redis = await get_redis()
    key = f"token:{message.from_user.id}"
    token = await redis.get(key)

    if not token:
        await message.answer(
            "Вы не авторизованы. Отправьте /token <JWT>, чтобы войти.\n"
            "Получить токен можно в Swagger Auth Service."
        )
        return

    try:
        decode_and_validate(token)
    except ValueError:
        await message.answer(
            "Токен истёк или недействителен. Получите новый в Auth Service и отправьте /token <JWT>."
        )
        return

    llm_request.delay(message.chat.id, message.text)
    await message.answer("Запрос принят, ожидаю ответ от LLM...")
