"""
Configuração principal do MILAPP Backend
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Configurações básicas
    APP_NAME: str = "MILAPP"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/milapp"
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = None
    LANGCHAIN_API_KEY: Optional[str] = None
    
    # Azure Integration
    AZURE_TENANT_ID: Optional[str] = None
    AZURE_CLIENT_ID: Optional[str] = None
    AZURE_CLIENT_SECRET: Optional[str] = None
    
    # Notifications
    TEAMS_WEBHOOK_URL: Optional[str] = None
    WHATSAPP_API_KEY: Optional[str] = None
    EMAIL_SERVER: Optional[str] = None
    EMAIL_USERNAME: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None
    
    # External Tools
    N8N_BASE_URL: Optional[str] = None
    N8N_API_KEY: Optional[str] = None
    POWERBI_WORKSPACE_ID: Optional[str] = None
    POWERBI_CLIENT_ID: Optional[str] = None
    POWERBI_CLIENT_SECRET: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File Storage
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = None
    AZURE_STORAGE_CONTAINER: str = "milapp-files"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8501"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância global das configurações
settings = Settings()