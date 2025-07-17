# 🐳 Docker - MILAPP

Este documento explica como executar o MILAPP usando Docker.

## 📋 Pré-requisitos

- Docker Desktop instalado
- Docker Compose instalado
- 8GB+ de RAM disponível
- 10GB+ de espaço em disco

## 🚀 Execução Rápida

### 1. Clone o repositório
```bash
git clone <repository-url>
cd milapp
```

### 2. Configure as variáveis de ambiente
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

### 3. Execute com Docker Compose
```bash
docker-compose up -d
```

### 4. Acesse as aplicações
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090
- **MinIO Console**: http://localhost:9001

## 🏗️ Estrutura dos Containers

### Frontend (React)
- **Porta**: 3000
- **Imagem**: nginx:alpine
- **Build**: Multi-stage com Node.js 18
- **Proxy**: Configurado para backend

### Backend (FastAPI)
- **Porta**: 8000
- **Imagem**: Python 3.11
- **Dependências**: Redis, MinIO
- **Health Check**: /health

### Redis
- **Porta**: 6379
- **Persistência**: Volume docker
- **Uso**: Cache e sessões

### MinIO
- **Porta**: 9000 (API), 9001 (Console)
- **Persistência**: Volume docker
- **Uso**: Armazenamento de arquivos

### Prometheus
- **Porta**: 9090
- **Persistência**: Volume docker
- **Uso**: Métricas e monitoramento

### Grafana
- **Porta**: 3001
- **Credenciais**: admin/admin
- **Uso**: Dashboards e visualizações

## 🔧 Comandos Úteis

### Ver logs
```bash
# Todos os serviços
docker-compose logs -f

# Serviço específico
docker-compose logs -f frontend
docker-compose logs -f backend
```

### Rebuild de um serviço
```bash
# Frontend
docker-compose build frontend
docker-compose up -d frontend

# Backend
docker-compose build backend
docker-compose up -d backend
```

### Executar comandos dentro dos containers
```bash
# Frontend
docker-compose exec frontend sh

# Backend
docker-compose exec backend bash

# Redis
docker-compose exec redis redis-cli
```

### Parar todos os serviços
```bash
docker-compose down
```

### Parar e remover volumes
```bash
docker-compose down -v
```

## 📊 Monitoramento

### Health Checks
- **Frontend**: http://localhost:3000/health
- **Backend**: http://localhost:8000/health
- **Prometheus**: http://localhost:9090/-/healthy

### Métricas
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001

## 🛠️ Desenvolvimento

### Modo de desenvolvimento
```bash
# Frontend (com hot reload)
cd frontend
npm install
npm start

# Backend (com hot reload)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Build local
```bash
# Frontend
cd frontend
./build.sh  # Linux/Mac
build.bat   # Windows

# Backend
cd backend
docker build -t milapp-backend .
```

## 🔒 Segurança

### Variáveis de ambiente obrigatórias
```bash
# Backend
SECRET_KEY=your-secret-key
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key

# MinIO
MINIO_ACCESS_KEY=your-minio-access-key
MINIO_SECRET_KEY=your-minio-secret-key
MINIO_BUCKET_NAME=milapp-files

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Volumes persistentes
- `redis_data`: Dados do Redis
- `minio_data`: Arquivos do MinIO
- `prometheus_data`: Métricas do Prometheus
- `grafana_data`: Dashboards do Grafana
- `milapp_files`: Uploads da aplicação

## 🐛 Troubleshooting

### Problemas comuns

#### 1. Porta já em uso
```bash
# Verificar portas em uso
netstat -tulpn | grep :3000
netstat -tulpn | grep :8000

# Parar serviços conflitantes
sudo systemctl stop nginx  # se necessário
```

#### 2. Erro de permissão
```bash
# Linux/Mac
sudo chown -R $USER:$USER .

# Windows
# Executar como administrador
```

#### 3. Container não inicia
```bash
# Verificar logs
docker-compose logs frontend
docker-compose logs backend

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

#### 4. Problemas de rede
```bash
# Verificar redes Docker
docker network ls

# Limpar redes não utilizadas
docker network prune
```

## 📈 Performance

### Otimizações recomendadas
- **CPU**: 4+ cores
- **RAM**: 8GB+ (16GB recomendado)
- **Disco**: SSD recomendado
- **Rede**: Conexão estável

### Monitoramento de recursos
```bash
# Uso de recursos
docker stats

# Uso de disco
docker system df
```

## 🔄 Atualizações

### Atualizar imagens
```bash
docker-compose pull
docker-compose up -d
```

### Atualizar código
```bash
git pull
docker-compose build
docker-compose up -d
```

## 📝 Logs

### Localização dos logs
- **Frontend**: `/var/log/nginx/` (dentro do container)
- **Backend**: Console do container
- **Redis**: Console do container
- **MinIO**: Console do container

### Configuração de logs
```bash
# Logs com timestamp
docker-compose logs -f --timestamps

# Logs de um período específico
docker-compose logs --since="2024-01-01T00:00:00"
```

## 🎯 Conclusão

O MILAPP está configurado para execução completa em Docker com:
- ✅ **Frontend** - React com Nginx
- ✅ **Backend** - FastAPI com Redis
- ✅ **Monitoramento** - Prometheus + Grafana
- ✅ **Armazenamento** - MinIO
- ✅ **Cache** - Redis
- ✅ **Health Checks** - Todos os serviços
- ✅ **Volumes persistentes** - Dados seguros

**Status: ✅ PRONTO PARA PRODUÇÃO** 