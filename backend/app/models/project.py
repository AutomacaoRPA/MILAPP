"""
Modelo de Projeto
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Text, DateTime, Integer, Float, Boolean, ForeignKey, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.sql import func

from app.core.database import Base

class Project(Base):
    """Modelo de Projeto"""
    
    __tablename__ = "projects"
    
    # Identificação
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Informações básicas
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String(50), default="automation")
    priority = Column(String(20), default="medium")
    methodology = Column(String(20), default="scrum")
    
    # Status e progresso
    status = Column(String(50), default="planning")
    
    # Relacionamentos
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"), nullable=True)
    
    # Métricas de negócio
    roi_target = Column(Numeric(10, 2), nullable=True)
    roi_actual = Column(Numeric(10, 2), nullable=True)
    estimated_effort = Column(Integer, nullable=True)  # horas
    actual_effort = Column(Integer, nullable=True)  # horas
    
    # Datas
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Configurações
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relacionamentos
    user = relationship("User", back_populates="projects")
    team = relationship("Team", back_populates="projects")
    conversations = relationship("Conversation", back_populates="project")
    documents = relationship("Document", back_populates="project")
    tickets = relationship("Ticket", back_populates="project")
    quality_gates = relationship("QualityGate", back_populates="project")
    deployments = relationship("Deployment", back_populates="project")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"
    
    @property
    def completion_percentage(self) -> float:
        """Calcular porcentagem de conclusão"""
        status_percentages = {
            "planning": 10,
            "development": 50,
            "testing": 80,
            "deployed": 100,
            "maintenance": 100,
            "cancelled": 0
        }
        return status_percentages.get(self.status, 0)
    
    @property
    def days_remaining(self) -> Optional[int]:
        """Calcular dias restantes"""
        if not self.end_date:
            return None
        
        remaining = self.end_date.date() - datetime.now().date()
        return max(0, remaining.days)
    
    @property
    def risk_level(self) -> str:
        """Calcular nível de risco"""
        if self.status == "cancelled":
            return "high"
        elif self.priority == "critical":
            return "high"
        elif self.priority == "high":
            return "medium"
        else:
            return "low"
    
    @property
    def roi_percentage(self) -> float:
        """Calcular ROI em porcentagem"""
        if not self.roi_target or self.roi_target == 0:
            return 0.0
        
        return ((self.roi_actual or 0) / self.roi_target) * 100
    
    def to_dict(self):
        """Convert project to dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "status": self.status,
            "priority": self.priority,
            "methodology": self.methodology,
            "team_id": str(self.team_id) if self.team_id else None,
            "created_by": str(self.created_by),
            "roi_target": float(self.roi_target) if self.roi_target else None,
            "roi_actual": float(self.roi_actual) if self.roi_actual else None,
            "estimated_effort": self.estimated_effort,
            "actual_effort": self.actual_effort,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 