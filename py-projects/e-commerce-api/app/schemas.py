from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from .models import AccessRole

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: AccessRole
    is_email_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class EmailVerificationRequest(BaseModel):
    token: str