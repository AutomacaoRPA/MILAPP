"""
Router principal da API v1 do MILAPP
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    projects,
    conversations,
    documents,
    quality_gates,
    deployments,
    dashboards
)

# Criar router principal
api_router = APIRouter()

# Incluir todos os endpoints
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["Projects"]
)

api_router.include_router(
    conversations.router,
    prefix="/conversations",
    tags=["AI Conversations"]
)

api_router.include_router(
    documents.router,
    prefix="/documents",
    tags=["Documents"]
)

api_router.include_router(
    quality_gates.router,
    prefix="/quality-gates",
    tags=["Quality Gates"]
)

api_router.include_router(
    deployments.router,
    prefix="/deployments",
    tags=["Deployments"]
)

api_router.include_router(
    dashboards.router,
    prefix="/dashboards",
    tags=["Dashboards"]
) 