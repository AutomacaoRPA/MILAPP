"""
MILAPP - Centro de Excelência em Automação RPA
Backend API Principal
"""

import os
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram
import structlog

from app.core.config import settings
from app.core.database import engine, Base
from app.core.security import get_current_user
from app.api.v1.router import api_router
from app.services.ai_service import AIService
from app.services.notification_service import NotificationService

# Configuração de logging
logger = structlog.get_logger()

# Métricas Prometheus
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle da aplicação"""
    # Startup
    logger.info("Iniciando MILAPP Backend")
    
    # Criar tabelas se não existirem
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Inicializar serviços
    await AIService.initialize()
    await NotificationService.initialize()
    
    logger.info("MILAPP Backend iniciado com sucesso")
    
    yield
    
    # Shutdown
    logger.info("Encerrando MILAPP Backend")
    await AIService.cleanup()
    await NotificationService.cleanup()

# Criação da aplicação FastAPI
app = FastAPI(
    title="MILAPP API",
    description="API do Centro de Excelência em Automação RPA",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de segurança
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Middleware de métricas
@app.middleware("http")
async def metrics_middleware(request, call_next):
    import time
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    REQUEST_LATENCY.observe(duration)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    return response

# Middleware de logging
@app.middleware("http")
async def logging_middleware(request, call_next):
    logger.info(
        "Request",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    
    response = await call_next(request)
    
    logger.info(
        "Response",
        status_code=response.status_code,
        method=request.method,
        url=str(request.url)
    )
    
    return response

# Incluir rotas da API
app.include_router(api_router, prefix="/api/v1")

# Health check
@app.get("/health")
async def health_check():
    """Health check da aplicação"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": "2025-01-01T00:00:00Z"
    }

# Ready check
@app.get("/ready")
async def ready_check():
    """Ready check para Kubernetes"""
    try:
        # Verificar conexão com banco
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        
        # Verificar serviços críticos
        ai_status = await AIService.check_health()
        notification_status = await NotificationService.check_health()
        
        if ai_status and notification_status:
            return {"status": "ready"}
        else:
            return JSONResponse(
                status_code=503,
                content={"status": "not ready", "services": {
                    "ai": ai_status,
                    "notifications": notification_status
                }}
            )
    except Exception as e:
        logger.error("Ready check failed", error=str(e))
        return JSONResponse(
            status_code=503,
            content={"status": "not ready", "error": str(e)}
        )

# Métricas Prometheus
@app.get("/metrics")
async def metrics():
    """Endpoint para métricas Prometheus"""
    from prometheus_client import generate_latest
    return generate_latest()

# Tratamento de erros global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handler global de exceções"""
    logger.error(
        "Unhandled exception",
        error=str(exc),
        method=request.method,
        url=str(request.url)
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Erro interno do servidor",
            "error": str(exc) if settings.DEBUG else "Erro interno"
        }
    )

# Rota raiz
@app.get("/")
async def root():
    """Rota raiz da API"""
    return {
        "message": "MILAPP - Centro de Excelência em Automação RPA",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    ) 