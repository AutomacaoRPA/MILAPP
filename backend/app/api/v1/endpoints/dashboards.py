"""
Endpoints de Dashboards e Analytics
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/dashboards", tags=["Dashboards"])

class DashboardMetric(BaseModel):
    name: str
    value: float
    unit: str
    trend: str  # 'up', 'down', 'stable'
    change_percentage: float
    target: Optional[float] = None

class DashboardWidget(BaseModel):
    id: str
    type: str  # 'metric', 'chart', 'table', 'list'
    title: str
    data: Dict[str, Any]
    config: Optional[Dict[str, Any]] = None

class DashboardResponse(BaseModel):
    id: str
    name: str
    description: str
    type: str  # 'executive', 'operational', 'technical', 'custom'
    widgets: List[DashboardWidget]
    last_updated: datetime

class AnalyticsFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    project_ids: Optional[List[str]] = None
    user_ids: Optional[List[str]] = None
    status: Optional[str] = None
    type: Optional[str] = None

@router.get("/executive", response_model=DashboardResponse)
async def get_executive_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter dashboard executivo"""
    try:
        dashboard_data = await AnalyticsService.get_executive_dashboard(
            db=db,
            user_id=current_user.id
        )
        
        return DashboardResponse(
            id="executive",
            name="Dashboard Executivo",
            description="Visão geral dos KPIs e métricas de negócio",
            type="executive",
            widgets=dashboard_data["widgets"],
            last_updated=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter dashboard executivo: {str(e)}"
        )

@router.get("/operational", response_model=DashboardResponse)
async def get_operational_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter dashboard operacional"""
    try:
        dashboard_data = await AnalyticsService.get_operational_dashboard(
            db=db,
            user_id=current_user.id
        )
        
        return DashboardResponse(
            id="operational",
            name="Dashboard Operacional",
            description="Métricas de performance e status em tempo real",
            type="operational",
            widgets=dashboard_data["widgets"],
            last_updated=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter dashboard operacional: {str(e)}"
        )

@router.get("/technical", response_model=DashboardResponse)
async def get_technical_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter dashboard técnico"""
    try:
        dashboard_data = await AnalyticsService.get_technical_dashboard(
            db=db,
            user_id=current_user.id
        )
        
        return DashboardResponse(
            id="technical",
            name="Dashboard Técnico",
            description="Métricas técnicas e de desenvolvimento",
            type="technical",
            widgets=dashboard_data["widgets"],
            last_updated=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter dashboard técnico: {str(e)}"
        )

@router.get("/custom/{dashboard_id}", response_model=DashboardResponse)
async def get_custom_dashboard(
    dashboard_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter dashboard customizado"""
    try:
        dashboard_data = await AnalyticsService.get_custom_dashboard(
            db=db,
            dashboard_id=dashboard_id,
            user_id=current_user.id
        )
        
        if not dashboard_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dashboard não encontrado"
            )
        
        return DashboardResponse(
            id=dashboard_id,
            name=dashboard_data["name"],
            description=dashboard_data["description"],
            type="custom",
            widgets=dashboard_data["widgets"],
            last_updated=dashboard_data["last_updated"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter dashboard customizado: {str(e)}"
        )

@router.get("/metrics/roi")
async def get_roi_metrics(
    period: str = Query("30d", regex="^(7d|30d|90d|1y|all)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter métricas de ROI"""
    try:
        roi_data = await AnalyticsService.get_roi_metrics(
            db=db,
            user_id=current_user.id,
            period=period
        )
        
        return roi_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter métricas de ROI: {str(e)}"
        )

@router.get("/metrics/productivity")
async def get_productivity_metrics(
    period: str = Query("30d", regex="^(7d|30d|90d|1y|all)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter métricas de produtividade"""
    try:
        productivity_data = await AnalyticsService.get_productivity_metrics(
            db=db,
            user_id=current_user.id,
            period=period
        )
        
        return productivity_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter métricas de produtividade: {str(e)}"
        )

@router.get("/metrics/quality")
async def get_quality_metrics(
    period: str = Query("30d", regex="^(7d|30d|90d|1y|all)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter métricas de qualidade"""
    try:
        quality_data = await AnalyticsService.get_quality_metrics(
            db=db,
            user_id=current_user.id,
            period=period
        )
        
        return quality_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter métricas de qualidade: {str(e)}"
        )

@router.get("/analytics/trends")
async def get_trends_analysis(
    metric: str = Query(..., regex="^(roi|productivity|quality|automation_count)$"),
    period: str = Query("90d", regex="^(30d|90d|180d|1y)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter análise de tendências"""
    try:
        trends_data = await AnalyticsService.get_trends_analysis(
            db=db,
            user_id=current_user.id,
            metric=metric,
            period=period
        )
        
        return trends_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter análise de tendências: {str(e)}"
        )

@router.get("/analytics/predictions")
async def get_predictions(
    metric: str = Query(..., regex="^(roi|productivity|quality|automation_count)$"),
    horizon: int = Query(30, ge=7, le=365),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter previsões baseadas em IA"""
    try:
        predictions_data = await AnalyticsService.get_predictions(
            db=db,
            user_id=current_user.id,
            metric=metric,
            horizon=horizon
        )
        
        return predictions_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter previsões: {str(e)}"
        )

@router.post("/reports/generate")
async def generate_report(
    report_type: str = Query(..., regex="^(executive|operational|technical|custom)$"),
    filters: AnalyticsFilter = None,
    format: str = Query("json", regex="^(json|pdf|excel)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Gerar relatório personalizado"""
    try:
        report_data = await AnalyticsService.generate_report(
            db=db,
            user_id=current_user.id,
            report_type=report_type,
            filters=filters.dict() if filters else {},
            format=format
        )
        
        return report_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar relatório: {str(e)}"
        )

@router.get("/alerts")
async def get_alerts(
    severity: Optional[str] = Query(None, regex="^(low|medium|high|critical)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter alertas ativos"""
    try:
        alerts_data = await AnalyticsService.get_alerts(
            db=db,
            user_id=current_user.id,
            severity=severity
        )
        
        return alerts_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter alertas: {str(e)}"
        )

@router.get("/kpis")
async def get_kpis(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter KPIs principais"""
    try:
        kpis_data = await AnalyticsService.get_kpis(
            db=db,
            user_id=current_user.id
        )
        
        return kpis_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter KPIs: {str(e)}"
        )

@router.get("/performance/real-time")
async def get_real_time_performance(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Obter métricas de performance em tempo real"""
    try:
        performance_data = await AnalyticsService.get_real_time_performance(
            db=db,
            user_id=current_user.id
        )
        
        return performance_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter performance em tempo real: {str(e)}"
        ) 