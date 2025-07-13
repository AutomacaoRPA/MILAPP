"""
Modelo de projeto do MILAPP
"""
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime, date

from ..core.database import Base


class Project(Base):
    """Modelo SQLAlchemy para projetos"""
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="planning")
    methodology = Column(String(50), default="scrum")
    
    # Relacionamentos
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=True)
    
    # Datas
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    
    # Configurações do projeto
    settings = Column(JSONB, default={})
    
    # Métricas
    estimated_hours = Column(Integer, default=0)
    actual_hours = Column(Integer, default=0)
    budget = Column(Integer, default=0)  # em centavos
    actual_cost = Column(Integer, default=0)
    
    # Status de qualidade
    quality_score = Column(Integer, default=0)  # 0-100
    risk_level = Column(String(20), default="low")  # low, medium, high, critical
    
    # Relacionamentos
    conversations = relationship("Conversation", back_populates="project")
    documents = relationship("Document", back_populates="project")
    user_stories = relationship("UserStory", back_populates="project")
    quality_gates = relationship("QualityGate", back_populates="project")
    deployments = relationship("Deployment", back_populates="project")


class Sprint(Base):
    """Modelo SQLAlchemy para sprints"""
    __tablename__ = "sprints"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    goal = Column(Text, nullable=True)
    
    # Datas
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    
    # Capacidade e métricas
    capacity = Column(Integer, default=0)  # horas
    velocity = Column(Integer, default=0)  # story points
    status = Column(String(50), default="planning")  # planning, active, completed
    
    # Relacionamentos
    user_stories = relationship("UserStory", back_populates="sprint")
    project = relationship("Project", back_populates="sprints")


class UserStory(Base):
    """Modelo SQLAlchemy para user stories"""
    __tablename__ = "user_stories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    sprint_id = Column(UUID(as_uuid=True), ForeignKey("sprints.id"), nullable=True)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    acceptance_criteria = Column(JSONB, default=[])
    
    # Estimativas
    story_points = Column(Integer, default=0)
    estimated_hours = Column(Integer, default=0)
    actual_hours = Column(Integer, default=0)
    
    # Priorização
    priority = Column(Integer, default=0)
    business_value = Column(Integer, default=0)
    
    # Status
    status = Column(String(50), default="backlog")  # backlog, todo, in_progress, testing, done
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Datas
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    project = relationship("Project", back_populates="user_stories")
    sprint = relationship("Sprint", back_populates="user_stories")


# Schemas Pydantic
class ProjectCreate(BaseModel):
    """Schema para criação de projeto"""
    name: str
    description: Optional[str] = None
    methodology: str = "scrum"
    team_id: Optional[uuid.UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    estimated_hours: int = 0
    budget: int = 0
    settings: Dict[str, Any] = {}


class ProjectUpdate(BaseModel):
    """Schema para atualização de projeto"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    methodology: Optional[str] = None
    team_id: Optional[uuid.UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    estimated_hours: Optional[int] = None
    budget: Optional[int] = None
    settings: Optional[Dict[str, Any]] = None
    quality_score: Optional[int] = None
    risk_level: Optional[str] = None


class ProjectResponse(BaseModel):
    """Schema para resposta de projeto"""
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    status: str
    methodology: str
    created_by: uuid.UUID
    team_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    estimated_hours: int
    actual_hours: int
    budget: int
    actual_cost: int
    quality_score: int
    risk_level: str
    
    class Config:
        from_attributes = True


class SprintCreate(BaseModel):
    """Schema para criação de sprint"""
    name: str
    goal: Optional[str] = None
    start_date: datetime
    end_date: datetime
    capacity: int = 0


class SprintUpdate(BaseModel):
    """Schema para atualização de sprint"""
    name: Optional[str] = None
    goal: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    capacity: Optional[int] = None
    velocity: Optional[int] = None
    status: Optional[str] = None


class SprintResponse(BaseModel):
    """Schema para resposta de sprint"""
    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    goal: Optional[str] = None
    start_date: datetime
    end_date: datetime
    capacity: int
    velocity: int
    status: str
    
    class Config:
        from_attributes = True


class UserStoryCreate(BaseModel):
    """Schema para criação de user story"""
    title: str
    description: Optional[str] = None
    acceptance_criteria: List[str] = []
    story_points: int = 0
    estimated_hours: int = 0
    priority: int = 0
    business_value: int = 0
    sprint_id: Optional[uuid.UUID] = None
    assigned_to: Optional[uuid.UUID] = None


class UserStoryUpdate(BaseModel):
    """Schema para atualização de user story"""
    title: Optional[str] = None
    description: Optional[str] = None
    acceptance_criteria: Optional[List[str]] = None
    story_points: Optional[int] = None
    estimated_hours: Optional[int] = None
    actual_hours: Optional[int] = None
    priority: Optional[int] = None
    business_value: Optional[int] = None
    status: Optional[str] = None
    sprint_id: Optional[uuid.UUID] = None
    assigned_to: Optional[uuid.UUID] = None


class UserStoryResponse(BaseModel):
    """Schema para resposta de user story"""
    id: uuid.UUID
    project_id: uuid.UUID
    sprint_id: Optional[uuid.UUID] = None
    title: str
    description: Optional[str] = None
    acceptance_criteria: List[str]
    story_points: int
    estimated_hours: int
    actual_hours: int
    priority: int
    business_value: int
    status: str
    assigned_to: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Status possíveis
PROJECT_STATUSES = [
    "planning",
    "development", 
    "testing",
    "deployed",
    "maintenance",
    "completed",
    "cancelled"
]

SPRINT_STATUSES = [
    "planning",
    "active",
    "completed"
]

USER_STORY_STATUSES = [
    "backlog",
    "todo",
    "in_progress", 
    "testing",
    "done"
]

RISK_LEVELS = [
    "low",
    "medium", 
    "high",
    "critical"
]