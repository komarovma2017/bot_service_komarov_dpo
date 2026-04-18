# Unit-тесты JWT валидации в Bot Service

from jose import jwt

from app.core.config import settings
from app.core.jwt import decode_and_validate


def test_decode_valid_token():
    """Корректный токен декодируется и содержит sub."""
    payload = {"sub": "user-1", "role": "user"}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

    result = decode_and_validate(token)
    assert result["sub"] == "user-1"
    assert result["role"] == "user"


def test_decode_garbage_token():
    """Мусорная строка вызывает ValueError."""
    import pytest

    with pytest.raises(ValueError):
        decode_and_validate("not.a.valid.token")


def test_decode_token_without_sub():
    """Токен без поля sub вызывает ValueError."""
    import pytest

    payload = {"role": "user"}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

    with pytest.raises(ValueError):
        decode_and_validate(token)
