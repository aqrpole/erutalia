"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# Health schemas
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None
    role: Optional[str] = None

# Chat schemas
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    history: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    response: str
    sources: Optional[List[Dict[str, Any]]] = None

# Conversation schemas
class ConversationCreate(BaseModel):
    title: str

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime
