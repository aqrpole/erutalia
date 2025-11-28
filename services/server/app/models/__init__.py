"""
SQLAlchemy models
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from app.utils.idgen import generate_ulid
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(26), primary_key=True, default=generate_ulid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(String(50), nullable=False, default="user")  # admin, user, viewer, editor
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String(26), primary_key=True, default=generate_ulid)
    user_id = Column(String(26), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Message(Base):
    __tablename__ = "messages"
    
    # id = Column(String(26), primary_key=True, default=generate_ulid)
    # conversation_id = Column(String(26), ForeignKey("conversations.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # user, assistant, system
    # content = Column(Text, nullable=False)
    # metadata = Column(JSON, nullable=True)  # Additional metadata like tokens, model used
    message_metadata = Column(JSON, nullable=True)  # Renamed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    conversation = relationship("Conversation", back_populates="messages")

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID, ForeignKey("conversations.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_user_message = Column(Boolean, nullable=False)
