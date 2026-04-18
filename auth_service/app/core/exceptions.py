# Кастомные HTTP-исключения Auth Service

from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    """Базовый класс для всех доменных исключений."""
    pass


class UserAlreadyExistsError(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="Пользователь с таким email уже существует")


class InvalidCredentialsError(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Неверные учётные данные")


class InvalidTokenError(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Недействительный токен")


class TokenExpiredError(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Токен истёк")


class UserNotFoundError(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Пользователь не найден")


class PermissionDeniedError(BaseHTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Недостаточно прав")
