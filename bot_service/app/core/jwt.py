# Валидация JWT в Bot Service — только проверка, без создания

from jose import JWTError, jwt

from app.core.config import settings


def decode_and_validate(token: str) -> dict:
    """Декодирует и валидирует JWT. Возвращает payload или бросает ValueError."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except JWTError:
        raise ValueError("Недействительный токен")

    if not payload.get("sub"):
        raise ValueError("В токене отсутствует поле sub")

    return payload
