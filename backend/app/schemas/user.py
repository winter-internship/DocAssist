from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID

from app.models.user import UserRole

# Shared properties
class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    is_active: Optional[bool] = True

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to receive via API on update
class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    profile_settings: Optional[dict] = None

class UserPasswordChange(BaseModel):
    current_password: str
    new_password: str

class UserInDBBase(UserBase):
    id: UUID
    role: UserRole
    
    class Config:
        from_attributes = True

# Additional properties to return via API
class UserRead(UserInDBBase):
    profile_settings: Optional[dict] = {}

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
