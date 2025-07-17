"""
Endpoints de Gestão de Projetos
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.project import Project
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    type: str = Field(default="automation", regex="^(automation|enhancement|maintenance)$")
    priority: str = Field(default="medium", regex="^(low|medium|high|critical)$")
    methodology: str = Field(default="scrum", regex="^(scrum|kanban|hybrid)$")
    roi_target: Optional[float] = None
    estimated_effort: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    type: Optional[str] = Field(None, regex="^(automation|enhancement|maintenance)$")
    priority: Optional[str] = Field(None, regex="^(low|medium|high|critical)$")
    methodology: Optional[str] = Field(None, regex="^(scrum|kanban|hybrid)$")
    status: Optional[str] = Field(None, regex="^(planning|development|testing|deployed|maintenance|cancelled)$")
    roi_target: Optional[float] = None
    roi_actual: Optional[float] = None
    estimated_effort: Optional[int] = None
    actual_effort: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectResponse(ProjectBase):
    id: str
    status: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    roi_actual: Optional[float] = None
    actual_effort: Optional[int] = None
    team_size: Optional[int] = None
    completion_percentage: Optional[float] = None

class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]
    total: int
    page: int
    size: int
    pages: int

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Criar novo projeto"""
    try:
        project = await ProjectService.create_project(
            db=db,
            project_data=project_data,
            created_by=current_user.id
        )
        
        return ProjectResponse(
            id=str(project.id),
            name=project.name,
            description=project.description,
            type=project.type,
            priority=project.priority,
            methodology=project.methodology,
            status=project.status,
            created_by=str(project.created_by),
            created_at=project.created_at,
            updated_at=project.updated_at,
            roi_target=project.roi_target,
            roi_actual=project.roi_actual,
            estimated_effort=project.estimated_effort,
            actual_effort=project.actual_effort,
            start_date=project.start_date,
            end_date=project.end_date
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar projeto: {str(e)}"
        )

@router.get("/", response_model=ProjectListResponse)
async def get_projects(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Listar projetos com filtros e paginação"""
    try:
        projects, total = await ProjectService.get_projects(
            db=db,
            user_id=current_user.id,
            page=page,
            size=size,
            status=status,
            type=type,
            priority=priority,
            search=search
        )
        
        project_responses = []
        for project in projects:
            project_responses.append(ProjectResponse(
                id=str(project.id),
                name=project.name,
                description=project.description,
                type=project.type,
                priority=project.priority,
                methodology=project.methodology,
                status=project.status,
                created_by=str(project.created_by),
                created_at=project.created_at,
                updated_at=project.updated_at,
                roi_target=project.roi_target,
                roi_actual=project.roi_actual,
                estimated_effort=project.estimated_effort,
                actual_effort=project.actual_effort,
                start_date=project.start_date,
                end_date=project.end_date
            ))
        
        pages = (total + size - 1) // size
        
        return ProjectListResponse(
            projects=project_responses,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar projetos: {str(e)}"
        )

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter detalhes de um projeto específico"""
    try:
        project = await ProjectService.get_project(
            db=db,
            project_id=project_id,
            user_id=current_user.id
        )
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado"
            )
        
        return ProjectResponse(
            id=str(project.id),
            name=project.name,
            description=project.description,
            type=project.type,
            priority=project.priority,
            methodology=project.methodology,
            status=project.status,
            created_by=str(project.created_by),
            created_at=project.created_at,
            updated_at=project.updated_at,
            roi_target=project.roi_target,
            roi_actual=project.roi_actual,
            estimated_effort=project.estimated_effort,
            actual_effort=project.actual_effort,
            start_date=project.start_date,
            end_date=project.end_date
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter projeto: {str(e)}"
        )

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Atualizar projeto"""
    try:
        project = await ProjectService.update_project(
            db=db,
            project_id=project_id,
            project_data=project_data,
            user_id=current_user.id
        )
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado"
            )
        
        return ProjectResponse(
            id=str(project.id),
            name=project.name,
            description=project.description,
            type=project.type,
            priority=project.priority,
            methodology=project.methodology,
            status=project.status,
            created_by=str(project.created_by),
            created_at=project.created_at,
            updated_at=project.updated_at,
            roi_target=project.roi_target,
            roi_actual=project.roi_actual,
            estimated_effort=project.estimated_effort,
            actual_effort=project.actual_effort,
            start_date=project.start_date,
            end_date=project.end_date
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar projeto: {str(e)}"
        )

@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Deletar projeto"""
    try:
        success = await ProjectService.delete_project(
            db=db,
            project_id=project_id,
            user_id=current_user.id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado"
            )
        
        return {"message": "Projeto deletado com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar projeto: {str(e)}"
        )

@router.get("/{project_id}/metrics")
async def get_project_metrics(
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter métricas do projeto"""
    try:
        metrics = await ProjectService.get_project_metrics(
            db=db,
            project_id=project_id,
            user_id=current_user.id
        )
        
        if not metrics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado"
            )
        
        return metrics
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter métricas: {str(e)}"
        )

@router.post("/{project_id}/duplicate")
async def duplicate_project(
    project_id: str,
    new_name: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Duplicar projeto"""
    try:
        new_project = await ProjectService.duplicate_project(
            db=db,
            project_id=project_id,
            new_name=new_name,
            user_id=current_user.id
        )
        
        if not new_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado"
            )
        
        return {
            "message": "Projeto duplicado com sucesso",
            "new_project_id": str(new_project.id)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao duplicar projeto: {str(e)}"
        )

@router.get("/dashboard/summary")
async def get_projects_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter resumo dos projetos para dashboard"""
    try:
        summary = await ProjectService.get_projects_summary(
            db=db,
            user_id=current_user.id
        )
        
        return summary
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter resumo: {str(e)}"
        ) 