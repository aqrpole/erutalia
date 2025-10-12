# services/auth-service/app/models/user.py
from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.core.database import Base
from app.utils.idgen import generate_ulid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(26), primary_key=True, default=generate_ulid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200))
    role = Column(String(50), nullable=False, default="user")  # admin, user, viewer, editor
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(String(26), primary_key=True, default=generate_ulid)
    user_id = Column(String(26), nullable=False, index=True)
    token = Column(String(512), unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())