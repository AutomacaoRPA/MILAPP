"""
Sistema de segurança do MILAPP
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Configuração de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do JWT
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar senha"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gerar hash da senha"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Criar token de acesso JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Criar token de refresh JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verificar token JWT"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Obter usuário atual baseado no token"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Aqui você buscaria o usuário no banco de dados
    # Por enquanto, retornamos um usuário mock
    from app.models.user import User
    user = await User.get_by_id(user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(current_user = Depends(get_current_user)):
    """Obter usuário ativo atual"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    return current_user


# Azure AD Integration
class AzureADAuth:
    """Integração com Azure AD"""
    
    def __init__(self):
        self.tenant_id = settings.AZURE_TENANT_ID
        self.client_id = settings.AZURE_CLIENT_ID
        self.client_secret = settings.AZURE_CLIENT_SECRET
    
    async def validate_azure_token(self, token: str) -> Optional[dict]:
        """Validar token do Azure AD"""
        try:
            import msal
            
            # Configurar aplicação MSAL
            app = msal.ConfidentialClientApplication(
                client_id=self.client_id,
                client_credential=self.client_secret,
                authority=f"https://login.microsoftonline.com/{self.tenant_id}"
            )
            
            # Validar token
            result = app.acquire_token_silent(
                scopes=["https://graph.microsoft.com/.default"],
                account=None
            )
            
            if result:
                return result
            else:
                return None
                
        except Exception as e:
            logger.error("Azure AD token validation failed", error=str(e))
            return None
    
    async def get_user_info_from_azure(self, access_token: str) -> Optional[dict]:
        """Obter informações do usuário do Azure AD"""
        try:
            import httpx
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://graph.microsoft.com/v1.0/me",
                    headers=headers
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error("Failed to get user info from Azure AD", status_code=response.status_code)
                    return None
                    
        except Exception as e:
            logger.error("Azure AD user info request failed", error=str(e))
            return None


# Rate Limiting
class RateLimiter:
    """Sistema de rate limiting"""
    
    def __init__(self):
        self.redis_client = None  # Será inicializado com Redis
    
    async def check_rate_limit(self, user_id: str, endpoint: str) -> bool:
        """Verificar rate limit para usuário e endpoint"""
        try:
            import redis
            from datetime import datetime
            
            if not self.redis_client:
                self.redis_client = redis.Redis.from_url(settings.REDIS_URL)
            
            # Chave para rate limiting
            minute_key = f"rate_limit:{user_id}:{endpoint}:minute"
            hour_key = f"rate_limit:{user_id}:{endpoint}:hour"
            
            current_time = datetime.now()
            
            # Verificar limite por minuto
            minute_count = self.redis_client.get(minute_key)
            if minute_count and int(minute_count) >= settings.RATE_LIMIT_PER_MINUTE:
                return False
            
            # Verificar limite por hora
            hour_count = self.redis_client.get(hour_key)
            if hour_count and int(hour_count) >= settings.RATE_LIMIT_PER_HOUR:
                return False
            
            # Incrementar contadores
            pipe = self.redis_client.pipeline()
            pipe.incr(minute_key)
            pipe.expire(minute_key, 60)  # Expira em 1 minuto
            pipe.incr(hour_key)
            pipe.expire(hour_key, 3600)  # Expira em 1 hora
            pipe.execute()
            
            return True
            
        except Exception as e:
            logger.error("Rate limiting check failed", error=str(e))
            return True  # Em caso de erro, permitir acesso


# Auditoria
class AuditLogger:
    """Sistema de auditoria"""
    
    @staticmethod
    async def log_action(
        user_id: str,
        action: str,
        resource_type: str = None,
        resource_id: str = None,
        details: dict = None,
        ip_address: str = None
    ):
        """Registrar ação de auditoria"""
        try:
            from app.models.audit_log import AuditLog
            
            audit_log = AuditLog(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details or {},
                ip_address=ip_address,
                timestamp=datetime.utcnow()
            )
            
            # Salvar no banco de dados
            # await audit_log.save()
            
            logger.info(
                "Audit log",
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address=ip_address
            )
            
        except Exception as e:
            logger.error("Audit logging failed", error=str(e))


# Criptografia de dados sensíveis
class DataEncryption:
    """Criptografia de dados sensíveis"""
    
    def __init__(self):
        from cryptography.fernet import Fernet
        self.cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode())
    
    def encrypt_data(self, data: str) -> str:
        """Criptografar dados"""
        try:
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            return encrypted_data.decode()
        except Exception as e:
            logger.error("Data encryption failed", error=str(e))
            return data
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Descriptografar dados"""
        try:
            decrypted_data = self.cipher_suite.decrypt(encrypted_data.encode())
            return decrypted_data.decode()
        except Exception as e:
            logger.error("Data decryption failed", error=str(e))
            return encrypted_data


# Middleware de segurança
async def security_middleware(request, call_next):
    """Middleware de segurança"""
    # Verificar headers de segurança
    response = await call_next(request)
    
    # Adicionar headers de segurança
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    return response


# Função para verificar permissões
async def check_permission(user, resource_type: str, action: str) -> bool:
    """Verificar se usuário tem permissão para ação"""
    try:
        # Implementar lógica de verificação de permissões
        # Por enquanto, retornar True para usuários autenticados
        return user is not None
    except Exception as e:
        logger.error("Permission check failed", error=str(e))
        return False


# Decorator para verificar permissões
def require_permission(resource_type: str, action: str):
    """Decorator para verificar permissões"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuário não autenticado"
                )
            
            has_permission = await check_permission(current_user, resource_type, action)
            if not has_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permissão negada"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator 