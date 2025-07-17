"""
Serviço de Autenticação
"""

import os
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.user import User
from app.core.database import get_db

# Configuração de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Serviço de autenticação"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verificar senha"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Gerar hash da senha"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Criar token de acesso"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
        """Autenticar usuário com email e senha"""
        try:
            # Buscar usuário por email
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            
            if not user:
                return None
            
            if not AuthService.verify_password(password, user.hashed_password):
                return None
            
            # Atualizar último login
            user.last_login = datetime.utcnow()
            await db.commit()
            
            return user
            
        except Exception as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Obter usuário por email"""
        try:
            result = await db.execute(select(User).where(User.email == email))
            return result.scalar_one_or_none()
        except Exception as e:
            raise e
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: dict) -> User:
        """Criar novo usuário"""
        try:
            hashed_password = AuthService.get_password_hash(user_data["password"])
            
            user = User(
                email=user_data["email"],
                name=user_data["name"],
                hashed_password=hashed_password,
                role=user_data.get("role", "user"),
                department=user_data.get("department"),
                is_active=True
            )
            
            db.add(user)
            await db.commit()
            await db.refresh(user)
            
            return user
            
        except Exception as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def get_azure_login_url() -> str:
        """Gerar URL de login do Azure AD"""
        try:
            # Parâmetros para Azure AD
            client_id = settings.AZURE_CLIENT_ID
            redirect_uri = f"{settings.BACKEND_URL}/api/v1/auth/azure-callback"
            state = secrets.token_urlsafe(32)
            
            # Construir URL de autorização
            auth_url = (
                f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}/oauth2/v2.0/authorize?"
                f"client_id={client_id}&"
                f"response_type=code&"
                f"redirect_uri={redirect_uri}&"
                f"scope=openid%20profile%20email&"
                f"state={state}"
            )
            
            return auth_url
            
        except Exception as e:
            raise Exception(f"Erro ao gerar URL de login Azure: {str(e)}")
    
    @staticmethod
    async def get_azure_token(code: str) -> Dict[str, Any]:
        """Trocar código por token do Azure AD"""
        try:
            token_url = f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}/oauth2/v2.0/token"
            
            data = {
                "client_id": settings.AZURE_CLIENT_ID,
                "client_secret": settings.AZURE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": f"{settings.BACKEND_URL}/api/v1/auth/azure-callback"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=data)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            raise Exception(f"Erro ao obter token Azure: {str(e)}")
    
    @staticmethod
    async def get_azure_user_info(access_token: str) -> Dict[str, Any]:
        """Obter informações do usuário do Azure AD"""
        try:
            user_info_url = "https://graph.microsoft.com/v1.0/me"
            headers = {"Authorization": f"Bearer {access_token}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(user_info_url, headers=headers)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            raise Exception(f"Erro ao obter informações do usuário Azure: {str(e)}")
    
    @staticmethod
    async def create_or_update_azure_user(db: AsyncSession, user_info: Dict[str, Any]) -> User:
        """Criar ou atualizar usuário do Azure AD"""
        try:
            email = user_info.get("mail") or user_info.get("userPrincipalName")
            name = user_info.get("displayName", "")
            
            # Verificar se usuário já existe
            existing_user = await AuthService.get_user_by_email(db, email)
            
            if existing_user:
                # Atualizar informações
                existing_user.name = name
                existing_user.last_login = datetime.utcnow()
                existing_user.azure_id = user_info.get("id")
                await db.commit()
                await db.refresh(existing_user)
                return existing_user
            else:
                # Criar novo usuário
                user = User(
                    email=email,
                    name=name,
                    hashed_password="",  # Usuários Azure não têm senha local
                    role="user",
                    is_active=True,
                    azure_id=user_info.get("id")
                )
                
                db.add(user)
                await db.commit()
                await db.refresh(user)
                return user
                
        except Exception as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def create_password_reset_token(email: str) -> str:
        """Criar token de reset de senha"""
        try:
            # Gerar token único
            token = secrets.token_urlsafe(32)
            
            # Armazenar token no Redis (implementar se necessário)
            # await redis.set(f"password_reset:{token}", email, ex=3600)  # 1 hora
            
            return token
            
        except Exception as e:
            raise Exception(f"Erro ao criar token de reset: {str(e)}")
    
    @staticmethod
    async def verify_password_reset_token(token: str) -> Optional[str]:
        """Verificar token de reset de senha"""
        try:
            # Buscar token no Redis (implementar se necessário)
            # email = await redis.get(f"password_reset:{token}")
            
            # Mock para demonstração
            email = "test@example.com"  # Implementar busca real
            
            if email:
                # Deletar token após uso
                # await redis.delete(f"password_reset:{token}")
                return email
            
            return None
            
        except Exception as e:
            raise Exception(f"Erro ao verificar token de reset: {str(e)}")
    
    @staticmethod
    async def update_user_password(db: AsyncSession, email: str, new_password: str) -> bool:
        """Atualizar senha do usuário"""
        try:
            user = await AuthService.get_user_by_email(db, email)
            if not user:
                return False
            
            user.hashed_password = AuthService.get_password_hash(new_password)
            user.password_last_changed = datetime.utcnow()
            
            await db.commit()
            return True
            
        except Exception as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def send_password_reset_email(email: str, token: str) -> bool:
        """Enviar email de reset de senha"""
        try:
            # Implementar envio de email
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
            
            # Mock para demonstração
            print(f"Email de reset enviado para {email}: {reset_url}")
            
            return True
            
        except Exception as e:
            raise Exception(f"Erro ao enviar email de reset: {str(e)}")
    
    @staticmethod
    async def logout_user(db: AsyncSession, user_id: str) -> bool:
        """Logout do usuário"""
        try:
            # Implementar blacklist de tokens se necessário
            # await redis.set(f"blacklist:{token}", "true", ex=3600)
            
            return True
            
        except Exception as e:
            raise Exception(f"Erro no logout: {str(e)}")
    
    @staticmethod
    async def check_user_permissions(user: User, resource: str, action: str) -> bool:
        """Verificar permissões do usuário"""
        try:
            # Implementar verificação de permissões baseada em RBAC
            if user.role == "admin":
                return True
            
            # Verificar permissões específicas
            permissions = {
                "projects": ["read", "write", "delete"],
                "conversations": ["read", "write"],
                "documents": ["read", "write"],
                "quality_gates": ["read", "approve"],
                "deployments": ["read", "deploy"],
                "dashboards": ["read"]
            }
            
            if resource in permissions and action in permissions[resource]:
                return True
            
            return False
            
        except Exception as e:
            raise Exception(f"Erro ao verificar permissões: {str(e)}") 