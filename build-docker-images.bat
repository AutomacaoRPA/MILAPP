@echo off
REM Script para build das imagens Docker do MILAPP
REM Frontend + Backend

echo 🐳 MILAPP - Build das Imagens Docker
echo ======================================

REM Verificar se o Docker está instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker não encontrado!
    echo 📥 Por favor, instale o Docker Desktop: https://www.docker.com/products/docker-desktop/
    echo 🔄 Após instalar, reinicie o terminal e execute este script novamente.
    pause
    exit /b 1
)

echo ✅ Docker detectado: 
docker --version

echo.
echo 🚀 Iniciando build das imagens...

REM Parar containers existentes
echo 📦 Parando containers existentes...
docker-compose down 2>nul

REM Limpar imagens antigas (opcional)
echo 🧹 Limpando imagens antigas...
docker image prune -f 2>nul

REM Build do Backend
echo.
echo 🔨 Build do Backend (FastAPI)...
docker build -t milapp-backend:latest ./backend
if %errorlevel% neq 0 (
    echo ❌ Erro no build do Backend
    pause
    exit /b 1
)
echo ✅ Backend buildado com sucesso!

REM Build do Frontend
echo.
echo 🔨 Build do Frontend (React)...
docker build -t milapp-frontend:latest ./frontend
if %errorlevel% neq 0 (
    echo ❌ Erro no build do Frontend
    pause
    exit /b 1
)
echo ✅ Frontend buildado com sucesso!

REM Build com Docker Compose (opcional)
echo.
echo 🔨 Build com Docker Compose...
docker-compose build
if %errorlevel% neq 0 (
    echo ⚠️ Erro no Docker Compose, mas imagens individuais foram criadas
) else (
    echo ✅ Docker Compose buildado com sucesso!
)

REM Listar imagens criadas
echo.
echo 📋 Imagens criadas:
docker images | findstr milapp

echo.
echo 🎉 Build concluído com sucesso!
echo.
echo 📋 Comandos úteis:
echo   🚀 Executar: docker-compose up -d
echo   📊 Logs: docker-compose logs -f
echo   🛑 Parar: docker-compose down
echo   🧹 Limpar: docker-compose down -v
echo.
echo 🌐 URLs após execução:
echo   Frontend: http://localhost:3000
echo   Backend: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   Grafana: http://localhost:3001
echo   Prometheus: http://localhost:9090
echo.
pause 