#!/bin/bash

# Script para build das imagens Docker do MILAPP
# Frontend + Backend

echo "🐳 MILAPP - Build das Imagens Docker"
echo "======================================"

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado!"
    echo "📥 Por favor, instale o Docker: https://docs.docker.com/get-docker/"
    echo "🔄 Após instalar, reinicie o terminal e execute este script novamente."
    exit 1
fi

echo "✅ Docker detectado:"
docker --version

echo ""
echo "🚀 Iniciando build das imagens..."

# Parar containers existentes
echo "📦 Parando containers existentes..."
docker-compose down 2>/dev/null

# Limpar imagens antigas (opcional)
echo "🧹 Limpando imagens antigas..."
docker image prune -f 2>/dev/null

# Build do Backend
echo ""
echo "🔨 Build do Backend (FastAPI)..."
docker build -t milapp-backend:latest ./backend
if [ $? -ne 0 ]; then
    echo "❌ Erro no build do Backend"
    exit 1
fi
echo "✅ Backend buildado com sucesso!"

# Build do Frontend
echo ""
echo "🔨 Build do Frontend (React)..."
docker build -t milapp-frontend:latest ./frontend
if [ $? -ne 0 ]; then
    echo "❌ Erro no build do Frontend"
    exit 1
fi
echo "✅ Frontend buildado com sucesso!"

# Build com Docker Compose (opcional)
echo ""
echo "🔨 Build com Docker Compose..."
docker-compose build
if [ $? -ne 0 ]; then
    echo "⚠️ Erro no Docker Compose, mas imagens individuais foram criadas"
else
    echo "✅ Docker Compose buildado com sucesso!"
fi

# Listar imagens criadas
echo ""
echo "📋 Imagens criadas:"
docker images | grep milapp

echo ""
echo "🎉 Build concluído com sucesso!"
echo ""
echo "📋 Comandos úteis:"
echo "  🚀 Executar: docker-compose up -d"
echo "  📊 Logs: docker-compose logs -f"
echo "  🛑 Parar: docker-compose down"
echo "  🧹 Limpar: docker-compose down -v"
echo ""
echo "🌐 URLs após execução:"
echo "  Frontend: http://localhost:3000"
echo "  Backend: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo "  Grafana: http://localhost:3001"
echo "  Prometheus: http://localhost:9090"
echo "" 