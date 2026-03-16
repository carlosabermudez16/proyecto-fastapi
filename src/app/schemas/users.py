from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.schemas.items import ItemScheme


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserScheme(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    items: list[ItemScheme] = []

    class Config:
        from_attributes = True

class UserPublicScheme(UserBase):
    is_active: bool
    items: list[ItemScheme] = []

    class Config:
        from_attributes = True
