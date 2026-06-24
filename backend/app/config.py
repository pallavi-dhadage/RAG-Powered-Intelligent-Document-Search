from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    APP_NAME: str = "RAG Document Search"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/rag_db"
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    COLLECTION_NAME: str = "documents"
    
    REDIS_URL: str = "redis://localhost:6379"
    OPENAI_API_KEY: Optional[str] = None
    
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    
    MAX_FILE_SIZE: int = 10485760
    ALLOWED_EXTENSIONS: str = ".pdf,.txt,.docx,.doc"
    
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
