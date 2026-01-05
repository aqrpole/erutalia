"""
Configuration settings using Pydantic
"""
from pydantic_settings import BaseSettings
from pydantic          import Field, field_validator
from typing            import List, Optional
import os
from pathlib           import Path

class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    APP_NAME: str = "University LLM Chatbot API"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # CORS
    CORS_ORIGINS: List[str] = Field(default_factory=list)

    @field_validator("CORS_ORIGINS", mode="before")
    def split_cors(cls, v):
        """
        Parse comma-separated string from .env into a list.
        Handles empty strings safely.
        """
        if not v:
            return []
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30

    # Auth Service
    AUTH_SERVICE_URL: str = "localhost:8001"
    AUTH_REQUIRED: bool = True
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str

    # Ollama AWS
    OLLAMA_AWS_URL: str = "https://your-ollama-aws-endpoint.amazonaws.com"
    OLLAMA_API_KEY: str = "your-ollama-api-key"
    OLLAMA_MODEL: str = "llama2"
    EMBEDDING_MODEL: str = "all-minilm"
    EMBEDDING_DIM: int = 384  # all-minilm dimension

    # Qdrant
    QDRANT_URL: str
    QDRANT_COLLECTION: str = "university_documents"

    # Logging
    LOG_LEVEL: str = "INFO"

    # Bedrock Configuration
    BEDROCK_API_KEY: str
    BEDROCK_REGION: str = "us-east-1"  # Ohio region
    BEDROCK_MODEL_ID: str
    #BEDROCK_EMBEDDING_MODEL_ID embeddings generator for future use

    # Alternative: If using IAM credentials instead of API key
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    # Fallback to Ollama if Bedrock fails
    USE_BEDROCK: bool = True
    FALLBACK_TO_OLLAMA: bool = True

    class Config:
        # .env can be found auto by docker compose
        #env_file = ".env"
        #env_file = Path(__file__).resolve().parents[4] / ".env"
        case_sensitive = False

settings = Settings()
