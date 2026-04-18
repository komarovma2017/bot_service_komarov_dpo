# Эндпоинты Auth Service: /auth/register, /auth/login, /auth/me

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_uc, get_current_user
from app.db.models import User
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUsecase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=201)
async def register(body: RegisterRequest, uc: AuthUsecase = Depends(get_auth_uc)):
    user = await uc.register(body.email, body.password)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(form: OAuth2PasswordRequestForm = Depends(), uc: AuthUsecase = Depends(get_auth_uc)):
    token = await uc.login(form.username, form.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserPublic)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
