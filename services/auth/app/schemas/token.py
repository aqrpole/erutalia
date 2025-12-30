# services/auth/app/schemas/token.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None

class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None
    user_id: Optional[str] = None
    exp: Optional[datetime] = None

class LoginRequest(BaseModel):
    """Login request schema"""
    email   : EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str

class TokenRefreshResponse(BaseModel):
    """Token refresh response schema"""
    access_token: str
    token_type: str
    expires_in: Optional[int] = None
