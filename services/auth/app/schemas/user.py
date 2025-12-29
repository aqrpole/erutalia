# services/auth/app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema"""
    email    : EmailStr
    username : str
    full_name: Optional[str] = None
    role     : str = "user"   # ← add this with a default (AI didn't write this code)

class UserCreate(UserBase):
    """User creation schema"""
    password: str

class UserUpdate(BaseModel):
    """User update schema"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    """User response schema"""
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None  # <-- make this optional
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    """User schema for database operations"""
    hashed_password: str
