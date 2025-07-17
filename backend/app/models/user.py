"""
Modelo de Usuário do MILAPP
"""

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """Modelo de usuário"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    department = Column(String(100))
    role = Column(String(50), nullable=False, default="user")
    manager_id = Column(UUID(as_uuid=True), nullable=True)
    azure_id = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    preferences = Column(Text, default="{}")
    last_login = Column(DateTime(timezone=True), nullable=True)
    password_last_changed = Column(DateTime(timezone=True), nullable=True)
    mfa_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    projects = relationship("Project", back_populates="created_by_user")
    conversations = relationship("Conversation", back_populates="user")
    tickets = relationship("Ticket", back_populates="assigned_user")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    @classmethod
    async def get_by_id(cls, user_id: str):
        """Obter usuário por ID"""
        from sqlalchemy.ext.asyncio import AsyncSession
        from app.core.database import AsyncSessionLocal
        
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                "SELECT * FROM users WHERE id = :user_id",
                {"user_id": user_id}
            )
            user_data = result.fetchone()
            
            if user_data:
                user = cls()
                for key, value in user_data._mapping.items():
                    setattr(user, key, value)
                return user
            return None
    
    @classmethod
    async def get_by_email(cls, email: str):
        """Obter usuário por email"""
        from sqlalchemy.ext.asyncio import AsyncSession
        from app.core.database import AsyncSessionLocal
        
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                "SELECT * FROM users WHERE email = :email",
                {"email": email}
            )
            user_data = result.fetchone()
            
            if user_data:
                user = cls()
                for key, value in user_data._mapping.items():
                    setattr(user, key, value)
                return user
            return None
    
    @classmethod
    async def create_user(cls, user_data: dict):
        """Criar novo usuário"""
        from sqlalchemy.ext.asyncio import AsyncSession
        from app.core.database import AsyncSessionLocal
        
        async with AsyncSessionLocal() as session:
            user = cls(**user_data)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
    
    async def update_user(self, update_data: dict):
        """Atualizar usuário"""
        from sqlalchemy.ext.asyncio import AsyncSession
        from app.core.database import AsyncSessionLocal
        
        async with AsyncSessionLocal() as session:
            for key, value in update_data.items():
                setattr(self, key, value)
            self.updated_at = datetime.utcnow()
            session.add(self)
            await session.commit()
            await session.refresh(self)
            return self
    
    async def deactivate_user(self):
        """Desativar usuário"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
        return await self.update_user({"is_active": False})
    
    async def activate_user(self):
        """Ativar usuário"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
        return await self.update_user({"is_active": True})
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "department": self.department,
            "role": self.role,
            "manager_id": str(self.manager_id) if self.manager_id else None,
            "azure_id": self.azure_id,
            "is_active": self.is_active,
            "preferences": self.preferences,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "password_last_changed": self.password_last_changed.isoformat() if self.password_last_changed else None,
            "mfa_enabled": self.mfa_enabled,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


# Schemas Pydantic
class UserBase(BaseModel):
    """Schema base de usuário"""
    email: EmailStr
    name: str
    department: Optional[str] = None
    role: str = "user"
    manager_id: Optional[str] = None
    azure_id: Optional[str] = None
    is_active: bool = True
    preferences: dict = {}
    mfa_enabled: bool = False


class UserCreate(UserBase):
    """Schema para criação de usuário"""
    pass


class UserUpdate(BaseModel):
    """Schema para atualização de usuário"""
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    department: Optional[str] = None
    role: Optional[str] = None
    manager_id: Optional[str] = None
    azure_id: Optional[str] = None
    is_active: Optional[bool] = None
    preferences: Optional[dict] = None
    mfa_enabled: Optional[bool] = None


class UserResponse(UserBase):
    """Schema de resposta de usuário"""
    id: str
    last_login: Optional[str] = None
    password_last_changed: Optional[str] = None
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema para login de usuário"""
    email: EmailStr
    password: str


class UserPasswordChange(BaseModel):
    """Schema para mudança de senha"""
    current_password: str
    new_password: str
    confirm_password: str


class UserPreferences(BaseModel):
    """Schema para preferências do usuário"""
    theme: str = "light"
    language: str = "pt-BR"
    notifications: dict = {
        "email": True,
        "teams": True,
        "whatsapp": False
    }
    dashboard_layout: dict = {}
    automation_preferences: dict = {}


# Funções auxiliares
async def get_user_by_id(user_id: str) -> Optional[User]:
    """Obter usuário por ID"""
    return await User.get_by_id(user_id)


async def get_user_by_email(email: str) -> Optional[User]:
    """Obter usuário por email"""
    return await User.get_by_email(email)


async def create_user(user_data: dict) -> User:
    """Criar novo usuário"""
    return await User.create_user(user_data)


async def update_user(user: User, update_data: dict) -> User:
    """Atualizar usuário"""
    return await user.update_user(update_data)


async def get_users_by_department(department: str) -> List[User]:
    """Obter usuários por departamento"""
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.core.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            "SELECT * FROM users WHERE department = :department AND is_active = true",
            {"department": department}
        )
        users_data = result.fetchall()
        
        users = []
        for user_data in users_data:
            user = User()
            for key, value in user_data._mapping.items():
                setattr(user, key, value)
            users.append(user)
        
        return users


async def get_active_users() -> List[User]:
    """Obter todos os usuários ativos"""
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.core.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            "SELECT * FROM users WHERE is_active = true ORDER BY name"
        )
        users_data = result.fetchall()
        
        users = []
        for user_data in users_data:
            user = User()
            for key, value in user_data._mapping.items():
                setattr(user, key, value)
            users.append(user)
        
        return users


async def update_user_last_login(user_id: str):
    """Atualizar último login do usuário"""
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.core.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        await session.execute(
            "UPDATE users SET last_login = NOW() WHERE id = :user_id",
            {"user_id": user_id}
        )
        await session.commit() 