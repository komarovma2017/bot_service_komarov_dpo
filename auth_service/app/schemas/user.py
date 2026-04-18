# Публичное представление пользователя (без password_hash)

from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    id: str
    email: EmailStr
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}
