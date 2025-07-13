"""
Modelo de conversação do MILAPP (Módulo 1 - IA)
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime

from ..core.database import Base


class Conversation(Base):
    """Modelo SQLAlchemy para conversações"""
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    title = Column(String(255), nullable=False)
    status = Column(String(50), default="active")  # active, completed, archived
    
    # Análise IA
    ai_summary = Column(Text, nullable=True)
    extracted_requirements = Column(JSONB, default=[])
    confidence_score = Column(Integer, default=0)  # 0-100
    
    # Datas
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    project = relationship("Project", back_populates="conversations")
    user = relationship("User")


class Message(Base):
    """Modelo SQLAlchemy para mensagens"""
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    
    # Tipo de mensagem
    type = Column(String(50), nullable=False)  # text, image, pdf, audio, bpmn, system
    role = Column(String(20), nullable=False)  # user, assistant, system
    
    # Conteúdo
    content = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)  # em bytes
    file_type = Column(String(100), nullable=True)
    
    # Análise IA
    ai_analysis = Column(JSONB, default={})
    tokens_used = Column(Integer, default=0)
    processing_time = Column(Integer, default=0)  # em milissegundos
    
    # Status
    is_processed = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)
    
    # Datas
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    conversation = relationship("Conversation", back_populates="messages")


class ExtractedRequirement(Base):
    """Modelo SQLAlchemy para requisitos extraídos"""
    __tablename__ = "extracted_requirements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    
    # Tipo de requisito
    type = Column(String(50), nullable=False)  # objective, input, output, exception, system, stakeholder
    
    # Conteúdo
    description = Column(Text, nullable=False)
    details = Column(JSONB, default={})
    
    # Metadados
    confidence = Column(Integer, default=0)  # 0-100
    validated = Column(Boolean, default=False)
    validated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    validated_at = Column(DateTime(timezone=True), nullable=True)
    
    # Priorização
    priority = Column(Integer, default=0)
    complexity = Column(String(20), default="low")  # low, medium, high
    
    # Datas
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    conversation = relationship("Conversation")


# Schemas Pydantic
class ConversationCreate(BaseModel):
    """Schema para criação de conversação"""
    project_id: uuid.UUID
    title: str


class ConversationUpdate(BaseModel):
    """Schema para atualização de conversação"""
    title: Optional[str] = None
    status: Optional[str] = None
    ai_summary: Optional[str] = None
    extracted_requirements: Optional[List[Dict[str, Any]]] = None
    confidence_score: Optional[int] = None


class ConversationResponse(BaseModel):
    """Schema para resposta de conversação"""
    id: uuid.UUID
    project_id: uuid.UUID
    user_id: uuid.UUID
    title: str
    status: str
    ai_summary: Optional[str] = None
    extracted_requirements: List[Dict[str, Any]]
    confidence_score: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    message_count: int = 0
    
    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    """Schema para criação de mensagem"""
    type: str
    role: str
    content: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None


class MessageUpdate(BaseModel):
    """Schema para atualização de mensagem"""
    content: Optional[str] = None
    ai_analysis: Optional[Dict[str, Any]] = None
    is_processed: Optional[bool] = None
    error_message: Optional[str] = None


class MessageResponse(BaseModel):
    """Schema para resposta de mensagem"""
    id: uuid.UUID
    conversation_id: uuid.UUID
    type: str
    role: str
    content: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    ai_analysis: Dict[str, Any]
    tokens_used: int
    processing_time: int
    is_processed: bool
    error_message: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ExtractedRequirementCreate(BaseModel):
    """Schema para criação de requisito extraído"""
    type: str
    description: str
    details: Dict[str, Any] = {}
    confidence: int = 0
    priority: int = 0
    complexity: str = "low"


class ExtractedRequirementUpdate(BaseModel):
    """Schema para atualização de requisito extraído"""
    description: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    confidence: Optional[int] = None
    validated: Optional[bool] = None
    priority: Optional[int] = None
    complexity: Optional[str] = None


class ExtractedRequirementResponse(BaseModel):
    """Schema para resposta de requisito extraído"""
    id: uuid.UUID
    conversation_id: uuid.UUID
    type: str
    description: str
    details: Dict[str, Any]
    confidence: int
    validated: bool
    validated_by: Optional[uuid.UUID] = None
    validated_at: Optional[datetime] = None
    priority: int
    complexity: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Tipos de mensagem suportados
MESSAGE_TYPES = [
    "text",
    "image", 
    "pdf",
    "audio",
    "bpmn",
    "excel",
    "word",
    "system"
]

MESSAGE_ROLES = [
    "user",
    "assistant", 
    "system"
]

REQUIREMENT_TYPES = [
    "objective",
    "input",
    "output", 
    "exception",
    "system",
    "stakeholder",
    "process",
    "business_rule"
]

COMPLEXITY_LEVELS = [
    "low",
    "medium",
    "high"
]

CONVERSATION_STATUSES = [
    "active",
    "completed",
    "archived"
]