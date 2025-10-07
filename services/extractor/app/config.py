# services/extractor/app/config.py
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Extractor service configuration"""
    
    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "university_documents"
    
    # Ollama/Embeddings
    OLLAMA_URL: str = "http://localhost:11434"
    EMBEDDING_MODEL: str = "all-minilm"
    EMBEDDING_DIM: int = 384
    
    # Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    BATCH_SIZE: int = 100
    
    # Paths - SET YOUR FOLDER PATHS HERE
    INPUT_DIR: str = "app/data/input"  # CHANGE THIS LINE
    PROCESSED_DIR: str = "app/data/processed"   # CHANGE THIS LINE
    ERROR_LOG_DIR: str = "app/data/errors"  # CHANGE THIS LINE
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()