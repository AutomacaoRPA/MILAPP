"""
Configurações do MILAPP Backend
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    
    # Database Configuration (Supabase PostgreSQL)
    DATABASE_URL: Optional[str] = None
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Azure AD Configuration
    AZURE_TENANT_ID: Optional[str] = None
    AZURE_CLIENT_ID: Optional[str] = None
    AZURE_CLIENT_SECRET: Optional[str] = None
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = None
    LANGCHAIN_API_KEY: Optional[str] = None
    
    # External Integrations
    N8N_BASE_URL: Optional[str] = None
    N8N_API_KEY: Optional[str] = None
    
    # Notifications
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # File Storage (MinIO/S3)
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "milapp-files"
    MINIO_SECURE: bool = False
    
    # Monitoring
    PROMETHEUS_URL: Optional[str] = None
    GRAFANA_URL: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:3001"]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def database_url(self) -> str:
        """Get database URL from Supabase or direct DATABASE_URL"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        # Construct Supabase PostgreSQL URL
        # Extract host from SUPABASE_URL
        supabase_host = self.SUPABASE_URL.replace("https://", "").replace("http://", "")
        return f"postgresql://postgres:[YOUR-PASSWORD]@{supabase_host}:5432/postgres"

settings = Settings()


def get_settings() -> Settings:
    """Retorna as configurações da aplicação"""
    return settings 