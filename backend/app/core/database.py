"""
Configuração do banco de dados do MILAPP
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from supabase import create_client, Client
from redis import Redis
from typing import Optional

from .config import settings

# SQLAlchemy setup
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Supabase setup
supabase: Optional[Client] = None
if settings.SUPABASE_URL and settings.SUPABASE_KEY:
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Redis setup
redis_client: Optional[Redis] = None
if settings.REDIS_URL:
    redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_db():
    """Dependency para obter sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_supabase():
    """Dependency para obter cliente Supabase"""
    if not supabase:
        raise Exception("Supabase não configurado")
    return supabase


def get_redis():
    """Dependency para obter cliente Redis"""
    if not redis_client:
        raise Exception("Redis não configurado")
    return redis_client


# Função para criar tabelas
def create_tables():
    """Cria todas as tabelas no banco de dados"""
    Base.metadata.create_all(bind=engine)