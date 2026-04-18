# Зависимости FastAPI: БД, репозиторий, usecase, текущий пользователь

from typing import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenError, TokenExpiredError
from app.core.security import decode_token
from app.db.models import User
from app.db.session import AsyncSessionLocal
from app.repositories.users import UsersRepository
from app.usecases.auth import AuthUsecase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_users_repo(session: AsyncSession = Depends(get_db)) -> UsersRepository:
    return UsersRepository(session)


def get_auth_uc(repo: UsersRepository = Depends(get_users_repo)) -> AuthUsecase:
    return AuthUsecase(repo)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    repo: UsersRepository = Depends(get_users_repo),
) -> User:
    """Декодирует JWT и возвращает пользователя из БД."""
    try:
        payload = decode_token(token)
    except ValueError:
        raise InvalidTokenError()

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise InvalidTokenError()

    user = await repo.get_by_id(user_id)
    if not user:
        raise InvalidTokenError()

    return user
