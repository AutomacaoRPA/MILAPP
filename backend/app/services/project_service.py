"""
Serviço de Gestão de Projetos
"""

from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.models.user import User

class ProjectService:
    """Serviço de gestão de projetos"""
    
    @staticmethod
    async def create_project(
        db: AsyncSession,
        project_data: dict,
        created_by: str
    ) -> Project:
        """Criar novo projeto"""
        try:
            project = Project(
                name=project_data["name"],
                description=project_data.get("description"),
                type=project_data.get("type", "automation"),
                priority=project_data.get("priority", "medium"),
                methodology=project_data.get("methodology", "scrum"),
                status="planning",
                created_by=created_by,
                roi_target=project_data.get("roi_target"),
                estimated_effort=project_data.get("estimated_effort"),
                start_date=project_data.get("start_date"),
                end_date=project_data.get("end_date")
            )
            
            db.add(project)
            await db.commit()
            await db.refresh(project)
            
            return project
            
        except Exception as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def get_projects(
        db: AsyncSession,
        user_id: str,
        page: int = 1,
        size: int = 20,
        status: Optional[str] = None,
        type: Optional[str] = None,
        priority: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Project], int]:
        """Listar projetos com filtros e paginação"""
        try:
            # Construir query base
            query = select(Project).where(Project.created_by == user_id)
            
            # Aplicar filtros
            if status:
                query = query.where(Project.status == status)
            
            if type:
                query = query.where(Project.type == type)
            
            if priority:
                query = query.where(Project.priority == priority)
            
            if search:
                search_filter = or_(
                    Project.name.ilike(f"%{search}%"),
                    Project.description.ilike(f"%{search}%")
                )
                query = query.where(search_filter)
            
            # Contar total
            count_query = select(func.count()).select_from(query.subquery())
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            
            # Aplicar paginação
            offset = (page - 1) * size
            query = query.offset(offset).limit(size)
            
            # Ordenar por data de criação
            query = query.order_by(Project.created_at.desc())
            
            # Executar query
            result = await db.execute(query)
            projects = result.scalars().all()
            
            return projects, total
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def get_project(
        db: AsyncSession,
        project_id: str,
        user_id: str
    ) -> Optional[Project]:
        """Obter projeto específico"""
        try:
            query = select(Project).where(
                and_(
                    Project.id == project_id,
                    Project.created_by == user_id
                )
            )
            
            result = await db.execute(query)
            return result.scalar_one_or_none()
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def update_project(
        db: AsyncSession,
        project_id: str,
        project_data: dict,
        user_id: str
    ) -> Optional[Project]:
        """Atualizar projeto"""
        try:
            project = await ProjectService.get_project(db, project_id, user_id)
            if not project:
                return None
            
            # Atualizar campos
            for field, value in project_data.items():
                if value is not None and hasattr(project, field):
                    setattr(project, field, value)
            
            project.updated_at = datetime.utcnow()
            await db.commit()
            await db.refresh(project)
            
            return project
            
        except Exception as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def delete_project(
        db: AsyncSession,
        project_id: str,
        user_id: str
    ) -> bool:
        """Deletar projeto"""
        try:
            project = await ProjectService.get_project(db, project_id, user_id)
            if not project:
                return False
            
            await db.delete(project)
            await db.commit()
            
            return True
            
        except Exception as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def get_project_metrics(
        db: AsyncSession,
        project_id: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Obter métricas do projeto"""
        try:
            project = await ProjectService.get_project(db, project_id, user_id)
            if not project:
                return None
            
            # Calcular métricas básicas
            metrics = {
                "project_id": str(project.id),
                "name": project.name,
                "status": project.status,
                "completion_percentage": ProjectService._calculate_completion_percentage(project),
                "roi_current": project.roi_actual or 0,
                "roi_target": project.roi_target or 0,
                "effort_current": project.actual_effort or 0,
                "effort_estimated": project.estimated_effort or 0,
                "days_remaining": ProjectService._calculate_days_remaining(project),
                "risk_level": ProjectService._calculate_risk_level(project)
            }
            
            return metrics
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def duplicate_project(
        db: AsyncSession,
        project_id: str,
        new_name: str,
        user_id: str
    ) -> Optional[Project]:
        """Duplicar projeto"""
        try:
            original_project = await ProjectService.get_project(db, project_id, user_id)
            if not original_project:
                return None
            
            # Criar novo projeto baseado no original
            new_project = Project(
                name=new_name,
                description=original_project.description,
                type=original_project.type,
                priority=original_project.priority,
                methodology=original_project.methodology,
                status="planning",  # Reset status
                created_by=user_id,
                roi_target=original_project.roi_target,
                estimated_effort=original_project.estimated_effort,
                start_date=None,  # Reset dates
                end_date=None
            )
            
            db.add(new_project)
            await db.commit()
            await db.refresh(new_project)
            
            return new_project
            
        except Exception as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def get_projects_summary(
        db: AsyncSession,
        user_id: str
    ) -> Dict[str, Any]:
        """Obter resumo dos projetos para dashboard"""
        try:
            # Contar projetos por status
            status_counts = await ProjectService._get_project_counts_by_status(db, user_id)
            
            # Calcular métricas gerais
            total_projects = sum(status_counts.values())
            active_projects = status_counts.get("development", 0) + status_counts.get("testing", 0)
            completed_projects = status_counts.get("deployed", 0) + status_counts.get("maintenance", 0)
            
            # Calcular ROI médio
            avg_roi = await ProjectService._calculate_average_roi(db, user_id)
            
            # Projetos recentes
            recent_projects = await ProjectService._get_recent_projects(db, user_id, limit=5)
            
            summary = {
                "total_projects": total_projects,
                "active_projects": active_projects,
                "completed_projects": completed_projects,
                "status_distribution": status_counts,
                "average_roi": avg_roi,
                "recent_projects": recent_projects,
                "completion_rate": (completed_projects / total_projects * 100) if total_projects > 0 else 0
            }
            
            return summary
            
        except Exception as e:
            raise e
    
    @staticmethod
    def _calculate_completion_percentage(project: Project) -> float:
        """Calcular porcentagem de conclusão do projeto"""
        # Implementar lógica baseada em status e progresso
        status_percentages = {
            "planning": 10,
            "development": 50,
            "testing": 80,
            "deployed": 100,
            "maintenance": 100,
            "cancelled": 0
        }
        
        return status_percentages.get(project.status, 0)
    
    @staticmethod
    def _calculate_days_remaining(project: Project) -> Optional[int]:
        """Calcular dias restantes do projeto"""
        if not project.end_date:
            return None
        
        remaining = project.end_date - datetime.now().date()
        return max(0, remaining.days)
    
    @staticmethod
    def _calculate_risk_level(project: Project) -> str:
        """Calcular nível de risco do projeto"""
        # Implementar lógica de cálculo de risco
        if project.status == "cancelled":
            return "high"
        elif project.priority == "critical":
            return "high"
        elif project.priority == "high":
            return "medium"
        else:
            return "low"
    
    @staticmethod
    async def _get_project_counts_by_status(
        db: AsyncSession,
        user_id: str
    ) -> Dict[str, int]:
        """Obter contagem de projetos por status"""
        try:
            query = select(
                Project.status,
                func.count(Project.id)
            ).where(
                Project.created_by == user_id
            ).group_by(Project.status)
            
            result = await db.execute(query)
            counts = dict(result.all())
            
            return counts
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def _calculate_average_roi(
        db: AsyncSession,
        user_id: str
    ) -> float:
        """Calcular ROI médio dos projetos"""
        try:
            query = select(func.avg(Project.roi_actual)).where(
                and_(
                    Project.created_by == user_id,
                    Project.roi_actual.isnot(None)
                )
            )
            
            result = await db.execute(query)
            avg_roi = result.scalar()
            
            return float(avg_roi) if avg_roi else 0.0
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def _get_recent_projects(
        db: AsyncSession,
        user_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Obter projetos recentes"""
        try:
            query = select(Project).where(
                Project.created_by == user_id
            ).order_by(
                Project.created_at.desc()
            ).limit(limit)
            
            result = await db.execute(query)
            projects = result.scalars().all()
            
            return [
                {
                    "id": str(p.id),
                    "name": p.name,
                    "status": p.status,
                    "created_at": p.created_at.isoformat() if p.created_at else None
                }
                for p in projects
            ]
            
        except Exception as e:
            raise e 