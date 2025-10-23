# services/auth-service/app/core/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Auth Service Configuration"""

    # API Settings
    APP_NAME: str = "University LLM Chatbot - Auth Service"
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:chatbot321@postgres:5432/chatbot_auth"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30

    # JWT Settings
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Security
    BCRYPT_ROUNDS: int = 12

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000"
    ]

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
