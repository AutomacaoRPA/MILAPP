"""
Aplicação principal do MILAPP Backend
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .core.config import settings
from .core.database import create_tables
from .api.endpoints import conversations

# Cria aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistema Integrado de Gestão RPA e Inovação - MedSênior",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui routers
app.include_router(conversations.router, prefix="/api/v1")

# Configuração de arquivos estáticos
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuração de uploads
if os.path.exists("uploads"):
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.on_event("startup")
async def startup_event():
    """Evento executado na inicialização da aplicação"""
    try:
        # Cria tabelas se não existirem
        create_tables()
        print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} iniciado com sucesso!")
        print(f"📚 Documentação disponível em: http://localhost:8000/docs")
        print(f"🔧 ReDoc disponível em: http://localhost:8000/redoc")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar aplicação: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Evento executado no encerramento da aplicação"""
    print(f"🛑 {settings.APP_NAME} encerrado.")


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check da aplicação"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/api/v1/status")
async def api_status():
    """Status da API"""
    return {
        "api": "MILAPP API",
        "version": settings.APP_VERSION,
        "status": "operational",
        "modules": [
            "conversations",
            "projects", 
            "documents",
            "quality_gates",
            "user_stories",
            "deployments"
        ]
    }


# Tratamento de erros global
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Not Found",
        "message": "O recurso solicitado não foi encontrado",
        "path": str(request.url.path)
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal Server Error", 
        "message": "Erro interno do servidor",
        "path": str(request.url.path)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )