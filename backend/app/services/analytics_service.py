"""
Serviço de Analytics e Dashboards
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.models.user import User

class AnalyticsService:
    """Serviço de analytics e dashboards"""
    
    @staticmethod
    async def get_executive_dashboard(
        db: AsyncSession,
        user_id: str
    ) -> Dict[str, Any]:
        """Obter dashboard executivo"""
        try:
            # KPIs principais
            kpis = await AnalyticsService._get_main_kpis(db, user_id)
            
            # Gráficos de tendência
            trends = await AnalyticsService._get_trends_data(db, user_id)
            
            # Distribuição de projetos
            project_distribution = await AnalyticsService._get_project_distribution(db, user_id)
            
            # ROI por período
            roi_data = await AnalyticsService._get_roi_data(db, user_id)
            
            widgets = [
                {
                    "id": "main_kpis",
                    "type": "metrics",
                    "title": "KPIs Principais",
                    "data": kpis
                },
                {
                    "id": "trends_chart",
                    "type": "line_chart",
                    "title": "Tendências",
                    "data": trends
                },
                {
                    "id": "project_distribution",
                    "type": "pie_chart",
                    "title": "Distribuição de Projetos",
                    "data": project_distribution
                },
                {
                    "id": "roi_chart",
                    "type": "bar_chart",
                    "title": "ROI por Período",
                    "data": roi_data
                }
            ]
            
            return {"widgets": widgets}
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def get_operational_dashboard(
        db: AsyncSession,
        user_id: str
    ) -> Dict[str, Any]:
        """Obter dashboard operacional"""
        try:
            # Status em tempo real
            real_time_status = await AnalyticsService._get_real_time_status(db, user_id)
            
            # Performance por equipe
            team_performance = await AnalyticsService._get_team_performance(db, user_id)
            
            # Alertas ativos
            active_alerts = await AnalyticsService._get_active_alerts(db, user_id)
            
            # Métricas de qualidade
            quality_metrics = await AnalyticsService._get_quality_metrics(db, user_id)
            
            widgets = [
                {
                    "id": "real_time_status",
                    "type": "status_board",
                    "title": "Status em Tempo Real",
                    "data": real_time_status
                },
                {
                    "id": "team_performance",
                    "type": "table",
                    "title": "Performance por Equipe",
                    "data": team_performance
                },
                {
                    "id": "active_alerts",
                    "type": "alert_list",
                    "title": "Alertas Ativos",
                    "data": active_alerts
                },
                {
                    "id": "quality_metrics",
                    "type": "gauge_chart",
                    "title": "Métricas de Qualidade",
                    "data": quality_metrics
                }
            ]
            
            return {"widgets": widgets}
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def get_technical_dashboard(
        db: AsyncSession,
        user_id: str
    ) -> Dict[str, Any]:
        """Obter dashboard técnico"""
        try:
            # Métricas de desenvolvimento
            dev_metrics = await AnalyticsService._get_development_metrics(db, user_id)
            
            # Testes e qualidade
            test_metrics = await AnalyticsService._get_test_metrics(db, user_id)
            
            # Deploy e produção
            deployment_metrics = await AnalyticsService._get_deployment_metrics(db, user_id)
            
            # Performance técnica
            performance_metrics = await AnalyticsService._get_performance_metrics(db, user_id)
            
            widgets = [
                {
                    "id": "dev_metrics",
                    "type": "metrics",
                    "title": "Métricas de Desenvolvimento",
                    "data": dev_metrics
                },
                {
                    "id": "test_metrics",
                    "type": "chart",
                    "title": "Testes e Qualidade",
                    "data": test_metrics
                },
                {
                    "id": "deployment_metrics",
                    "type": "chart",
                    "title": "Deploy e Produção",
                    "data": deployment_metrics
                },
                {
                    "id": "performance_metrics",
                    "type": "chart",
                    "title": "Performance Técnica",
                    "data": performance_metrics
                }
            ]
            
            return {"widgets": widgets}
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def get_custom_dashboard(
        db: AsyncSession,
        dashboard_id: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Obter dashboard customizado"""
        try:
            # Implementar busca de dashboard customizado
            # Por enquanto, retorna None
            return None
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def get_roi_metrics(
        db: AsyncSession,
        user_id: str,
        period: str = "30d"
    ) -> Dict[str, Any]:
        """Obter métricas de ROI"""
        try:
            # Calcular período
            end_date = datetime.now()
            if period == "7d":
                start_date = end_date - timedelta(days=7)
            elif period == "30d":
                start_date = end_date - timedelta(days=30)
            elif period == "90d":
                start_date = end_date - timedelta(days=90)
            elif period == "1y":
                start_date = end_date - timedelta(days=365)
            else:
                start_date = datetime.min
            
            # Buscar projetos no período
            query = select(Project).where(
                and_(
                    Project.created_by == user_id,
                    Project.created_at >= start_date,
                    Project.created_at <= end_date
                )
            )
            
            result = await db.execute(query)
            projects = result.scalars().all()
            
            # Calcular métricas
            total_roi = sum(p.roi_actual or 0 for p in projects)
            avg_roi = total_roi / len(projects) if projects else 0
            total_investment = sum(p.estimated_effort or 0 for p in projects)
            total_return = total_roi + total_investment
            
            roi_percentage = (total_roi / total_investment * 100) if total_investment > 0 else 0
            
            return {
                "period": period,
                "total_roi": total_roi,
                "average_roi": avg_roi,
                "total_investment": total_investment,
                "total_return": total_return,
                "roi_percentage": roi_percentage,
                "project_count": len(projects)
            }
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def get_productivity_metrics(
        db: AsyncSession,
        user_id: str,
        period: str = "30d"
    ) -> Dict[str, Any]:
        """Obter métricas de produtividade"""
        try:
            # Calcular período
            end_date = datetime.now()
            if period == "7d":
                start_date = end_date - timedelta(days=7)
            elif period == "30d":
                start_date = end_date - timedelta(days=30)
            elif period == "90d":
                start_date = end_date - timedelta(days=90)
            elif period == "1y":
                start_date = end_date - timedelta(days=365)
            else:
                start_date = datetime.min
            
            # Buscar projetos no período
            query = select(Project).where(
                and_(
                    Project.created_by == user_id,
                    Project.created_at >= start_date,
                    Project.created_at <= end_date
                )
            )
            
            result = await db.execute(query)
            projects = result.scalars().all()
            
            # Calcular métricas de produtividade
            total_projects = len(projects)
            completed_projects = len([p for p in projects if p.status in ["deployed", "maintenance"]])
            completion_rate = (completed_projects / total_projects * 100) if total_projects > 0 else 0
            
            avg_effort = sum(p.actual_effort or 0 for p in projects) / len(projects) if projects else 0
            total_effort = sum(p.actual_effort or 0 for p in projects)
            
            return {
                "period": period,
                "total_projects": total_projects,
                "completed_projects": completed_projects,
                "completion_rate": completion_rate,
                "average_effort": avg_effort,
                "total_effort": total_effort,
                "projects_per_month": total_projects / (period_days / 30) if period_days > 0 else 0
            }
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def get_quality_metrics(
        db: AsyncSession,
        user_id: str,
        period: str = "30d"
    ) -> Dict[str, Any]:
        """Obter métricas de qualidade"""
        try:
            # Implementar métricas de qualidade
            # Por enquanto, retorna dados mock
            return {
                "period": period,
                "defect_rate": 2.5,
                "test_coverage": 85.0,
                "code_quality_score": 92.0,
                "customer_satisfaction": 4.2,
                "bug_fix_time": 3.5
            }
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def get_trends_analysis(
        db: AsyncSession,
        user_id: str,
        metric: str,
        period: str = "90d"
    ) -> Dict[str, Any]:
        """Obter análise de tendências"""
        try:
            # Implementar análise de tendências
            # Por enquanto, retorna dados mock
            return {
                "metric": metric,
                "period": period,
                "trend": "up",
                "change_percentage": 15.5,
                "data_points": [
                    {"date": "2025-01-01", "value": 100},
                    {"date": "2025-01-15", "value": 115},
                    {"date": "2025-01-30", "value": 130}
                ]
            }
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def get_predictions(
        db: AsyncSession,
        user_id: str,
        metric: str,
        horizon: int = 30
    ) -> Dict[str, Any]:
        """Obter previsões baseadas em IA"""
        try:
            # Implementar previsões com IA
            # Por enquanto, retorna dados mock
            return {
                "metric": metric,
                "horizon": horizon,
                "predictions": [
                    {"date": "2025-02-01", "value": 145, "confidence": 0.85},
                    {"date": "2025-02-15", "value": 160, "confidence": 0.80},
                    {"date": "2025-02-28", "value": 175, "confidence": 0.75}
                ],
                "model_accuracy": 0.87
            }
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def generate_report(
        db: AsyncSession,
        user_id: str,
        report_type: str,
        filters: Dict[str, Any],
        format: str = "json"
    ) -> Dict[str, Any]:
        """Gerar relatório personalizado"""
        try:
            # Implementar geração de relatórios
            # Por enquanto, retorna dados mock
            return {
                "report_type": report_type,
                "format": format,
                "generated_at": datetime.now().isoformat(),
                "data": {
                    "summary": "Relatório gerado com sucesso",
                    "metrics": {},
                    "charts": {},
                    "recommendations": []
                }
            }
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def get_alerts(
        db: AsyncSession,
        user_id: str,
        severity: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Obter alertas ativos"""
        try:
            # Implementar sistema de alertas
            # Por enquanto, retorna alertas mock
            alerts = [
                {
                    "id": "1",
                    "type": "performance",
                    "severity": "medium",
                    "title": "Projeto atrasado",
                    "description": "Projeto X está 5 dias atrasado",
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": "2",
                    "type": "quality",
                    "severity": "low",
                    "title": "Teste falhou",
                    "description": "Teste de integração falhou",
                    "created_at": datetime.now().isoformat()
                }
            ]
            
            if severity:
                alerts = [a for a in alerts if a["severity"] == severity]
            
            return alerts
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def get_kpis(
        db: AsyncSession,
        user_id: str
    ) -> Dict[str, Any]:
        """Obter KPIs principais"""
        try:
            # Calcular KPIs principais
            total_projects = await AnalyticsService._count_projects(db, user_id)
            active_projects = await AnalyticsService._count_active_projects(db, user_id)
            avg_roi = await AnalyticsService._calculate_average_roi(db, user_id)
            completion_rate = await AnalyticsService._calculate_completion_rate(db, user_id)
            
            return {
                "total_projects": total_projects,
                "active_projects": active_projects,
                "average_roi": avg_roi,
                "completion_rate": completion_rate,
                "productivity_score": 85.5,
                "quality_score": 92.0
            }
            
        except Exception as e:
            raise e
    
    @staticmethod
    async def get_real_time_performance(
        db: AsyncSession,
        user_id: str
    ) -> Dict[str, Any]:
        """Obter métricas de performance em tempo real"""
        try:
            # Implementar métricas em tempo real
            # Por enquanto, retorna dados mock
            return {
                "active_automations": 15,
                "success_rate": 98.5,
                "average_response_time": 2.3,
                "throughput": 150,
                "error_rate": 1.5,
                "uptime": 99.9
            }
            
        except Exception as e:
            raise e
    
    # Métodos auxiliares privados
    @staticmethod
    async def _get_main_kpis(db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """Obter KPIs principais"""
        try:
            total_projects = await AnalyticsService._count_projects(db, user_id)
            active_projects = await AnalyticsService._count_active_projects(db, user_id)
            avg_roi = await AnalyticsService._calculate_average_roi(db, user_id)
            
            return {
                "total_projects": total_projects,
                "active_projects": active_projects,
                "average_roi": avg_roi,
                "completion_rate": 75.5
            }
        except Exception as e:
            raise e
    
    @staticmethod
    async def _get_trends_data(db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """Obter dados de tendências"""
        # Mock data
        return {
            "labels": ["Jan", "Fev", "Mar", "Abr", "Mai"],
            "datasets": [
                {
                    "label": "Projetos",
                    "data": [10, 15, 20, 25, 30]
                }
            ]
        }
    
    @staticmethod
    async def _get_project_distribution(db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """Obter distribuição de projetos"""
        try:
            query = select(
                Project.status,
                func.count(Project.id)
            ).where(
                Project.created_by == user_id
            ).group_by(Project.status)
            
            result = await db.execute(query)
            distribution = dict(result.all())
            
            return {
                "labels": list(distribution.keys()),
                "data": list(distribution.values())
            }
        except Exception as e:
            raise e
    
    @staticmethod
    async def _get_roi_data(db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """Obter dados de ROI"""
        # Mock data
        return {
            "labels": ["Q1", "Q2", "Q3", "Q4"],
            "datasets": [
                {
                    "label": "ROI (%)",
                    "data": [15, 25, 30, 35]
                }
            ]
        }
    
    @staticmethod
    async def _get_real_time_status(db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """Obter status em tempo real"""
        # Mock data
        return {
            "running": 15,
            "stopped": 3,
            "error": 1,
            "maintenance": 2
        }
    
    @staticmethod
    async def _get_team_performance(db: AsyncSession, user_id: str) -> List[Dict[str, Any]]:
        """Obter performance por equipe"""
        # Mock data
        return [
            {"team": "Equipe A", "projects": 8, "completion_rate": 85},
            {"team": "Equipe B", "projects": 6, "completion_rate": 92},
            {"team": "Equipe C", "projects": 4, "completion_rate": 78}
        ]
    
    @staticmethod
    async def _get_active_alerts(db: AsyncSession, user_id: str) -> List[Dict[str, Any]]:
        """Obter alertas ativos"""
        # Mock data
        return [
            {"id": "1", "type": "warning", "message": "Projeto atrasado", "time": "2h ago"},
            {"id": "2", "type": "info", "message": "Deploy concluído", "time": "1h ago"}
        ]
    
    @staticmethod
    async def _get_quality_metrics(db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """Obter métricas de qualidade"""
        # Mock data
        return {
            "test_coverage": 85,
            "code_quality": 92,
            "defect_rate": 2.5,
            "customer_satisfaction": 4.2
        }
    
    @staticmethod
    async def _get_development_metrics(db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """Obter métricas de desenvolvimento"""
        # Mock data
        return {
            "velocity": 25,
            "cycle_time": 12,
            "lead_time": 18,
            "code_reviews": 95
        }
    
    @staticmethod
    async def _get_test_metrics(db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """Obter métricas de teste"""
        # Mock data
        return {
            "test_coverage": 85,
            "pass_rate": 98,
            "automated_tests": 150,
            "manual_tests": 25
        }
    
    @staticmethod
    async def _get_deployment_metrics(db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """Obter métricas de deploy"""
        # Mock data
        return {
            "deployments": 45,
            "success_rate": 96,
            "rollback_rate": 4,
            "deployment_time": 15
        }
    
    @staticmethod
    async def _get_performance_metrics(db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """Obter métricas de performance"""
        # Mock data
        return {
            "response_time": 2.3,
            "throughput": 150,
            "error_rate": 1.5,
            "uptime": 99.9
        }
    
    @staticmethod
    async def _count_projects(db: AsyncSession, user_id: str) -> int:
        """Contar total de projetos"""
        try:
            query = select(func.count(Project.id)).where(Project.created_by == user_id)
            result = await db.execute(query)
            return result.scalar()
        except Exception as e:
            raise e
    
    @staticmethod
    async def _count_active_projects(db: AsyncSession, user_id: str) -> int:
        """Contar projetos ativos"""
        try:
            query = select(func.count(Project.id)).where(
                and_(
                    Project.created_by == user_id,
                    Project.status.in_(["development", "testing"])
                )
            )
            result = await db.execute(query)
            return result.scalar()
        except Exception as e:
            raise e
    
    @staticmethod
    async def _calculate_average_roi(db: AsyncSession, user_id: str) -> float:
        """Calcular ROI médio"""
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
    async def _calculate_completion_rate(db: AsyncSession, user_id: str) -> float:
        """Calcular taxa de conclusão"""
        try:
            total_query = select(func.count(Project.id)).where(Project.created_by == user_id)
            completed_query = select(func.count(Project.id)).where(
                and_(
                    Project.created_by == user_id,
                    Project.status.in_(["deployed", "maintenance"])
                )
            )
            
            total_result = await db.execute(total_query)
            completed_result = await db.execute(completed_query)
            
            total = total_result.scalar()
            completed = completed_result.scalar()
            
            return (completed / total * 100) if total > 0 else 0.0
        except Exception as e:
            raise e 