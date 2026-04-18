# Unit-тесты: хеширование паролей и JWT

from app.core.security import create_access_token, decode_token, hash_password, verify_password


def test_hash_password():
    """Хеш не равен исходному паролю."""
    password = "secret123"
    hashed = hash_password(password)
    assert hashed != password


def test_verify_password_correct():
    """Правильный пароль проходит проверку."""
    password = "secret123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Неправильный пароль не проходит проверку."""
    hashed = hash_password("secret123")
    assert verify_password("wrong", hashed) is False


def test_create_and_decode_token():
    """Токен содержит sub, role, iat, exp."""
    token = create_access_token(sub="user-1", role="admin")
    payload = decode_token(token)

    assert payload["sub"] == "user-1"
    assert payload["role"] == "admin"
    assert "iat" in payload
    assert "exp" in payload


def test_decode_invalid_token():
    """Мусорная строка вызывает ValueError."""
    import pytest

    with pytest.raises(ValueError):
        decode_token("invalid.token.string")
