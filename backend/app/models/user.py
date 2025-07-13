"""
Modelo de usuário do MILAPP
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import uuid
from datetime import datetime

from ..core.database import Base


class User(Base):
    """Modelo SQLAlchemy para usuários"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="stakeholder")
    azure_id = Column(String(255), unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Campos adicionais para perfil
    department = Column(String(100), nullable=True)
    position = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Configurações de notificação
    email_notifications = Column(Boolean, default=True)
    teams_notifications = Column(Boolean, default=True)
    whatsapp_notifications = Column(Boolean, default=False)


class UserCreate(BaseModel):
    """Schema para criação de usuário"""
    email: EmailStr
    name: str
    role: str = "stakeholder"
    azure_id: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema para atualização de usuário"""
    name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    department: Optional[str] = None
    position: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    email_notifications: Optional[bool] = None
    teams_notifications: Optional[bool] = None
    whatsapp_notifications: Optional[bool] = None


class UserResponse(BaseModel):
    """Schema para resposta de usuário"""
    id: uuid.UUID
    email: str
    name: str
    role: str
    is_active: bool
    department: Optional[str] = None
    position: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Roles e permissões
ROLES = {
    "admin": {
        "description": "Administrador do sistema",
        "permissions": ["*"]  # Todas as permissões
    },
    "architect": {
        "description": "Arquiteto de soluções",
        "permissions": [
            "projects.*",
            "conversations.*",
            "documents.*",
            "quality_gates.*",
            "deployments.*",
            "users.read"
        ]
    },
    "po": {
        "description": "Product Owner",
        "permissions": [
            "projects.*",
            "conversations.*",
            "documents.*",
            "user_stories.*",
            "sprints.*",
            "quality_gates.read"
        ]
    },
    "developer": {
        "description": "Desenvolvedor",
        "permissions": [
            "projects.read",
            "user_stories.*",
            "code_artifacts.*",
            "tests.*",
            "deployments.read"
        ]
    },
    "qa": {
        "description": "Quality Assurance",
        "permissions": [
            "projects.read",
            "tests.*",
            "quality_gates.read",
            "deployments.read"
        ]
    },
    "stakeholder": {
        "description": "Stakeholder",
        "permissions": [
            "projects.read",
            "conversations.read",
            "documents.read",
            "dashboards.read"
        ]
    }
}


def has_permission(user_role: str, required_permission: str) -> bool:
    """Verifica se um usuário tem determinada permissão"""
    if user_role not in ROLES:
        return False
    
    user_permissions = ROLES[user_role]["permissions"]
    
    # Permissão wildcard
    if "*" in user_permissions:
        return True
    
    # Verificação específica
    if required_permission in user_permissions:
        return True
    
    # Verificação de padrão (ex: projects.*)
    for permission in user_permissions:
        if permission.endswith(".*"):
            base_permission = permission[:-2]
            if required_permission.startswith(base_permission):
                return True
    
    return False