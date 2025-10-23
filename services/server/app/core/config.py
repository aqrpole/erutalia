"""
Configuration settings using Pydantic
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    APP_NAME: str = "University LLM Chatbot API"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:chatbot321@postgres:5432/chatbot"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    
    # Auth Service
    AUTH_SERVICE_URL: str = "10.200.189.118:8001"
    AUTH_REQUIRED: bool = True
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Ollama AWS
    OLLAMA_AWS_URL: str = "https://your-ollama-aws-endpoint.amazonaws.com"
    OLLAMA_API_KEY: str = "your-ollama-api-key"
    OLLAMA_MODEL: str = "llama2"
    EMBEDDING_MODEL: str = "all-minilm"
    EMBEDDING_DIM: int = 384  # all-minilm dimension
    
    # Qdrant
    QDRANT_URL: str = "http://qdrant:6333"
    QDRANT_COLLECTION: str = "university_documents"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()