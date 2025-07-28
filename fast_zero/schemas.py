from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class UserRead(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class ItemSchema(BaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100