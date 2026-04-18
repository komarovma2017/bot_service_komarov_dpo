# Бизнес-логика Auth Service: регистрация, логин, профиль

from app.core.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories.users import UsersRepository


class AuthUsecase:
    def __init__(self, repo: UsersRepository):
        self.repo = repo

    async def register(self, email: str, password: str) -> User:
        """Регистрация нового пользователя."""
        existing = await self.repo.get_by_email(email)
        if existing:
            raise UserAlreadyExistsError()

        user = User(
            email=email,
            password_hash=hash_password(password),
        )
        return await self.repo.create(user)

    async def login(self, email: str, password: str) -> str:
        """Логин — возвращает JWT."""
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        return create_access_token(sub=user.id, role=user.role)

    async def me(self, user_id: str) -> User:
        """Возвращает профиль пользователя по id."""
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user
