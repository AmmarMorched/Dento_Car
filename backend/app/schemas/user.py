from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    phone: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str | None
    plan: str
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True