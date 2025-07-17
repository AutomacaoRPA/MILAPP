# 🐳 Build das Imagens Docker - MILAPP

## 📋 Pré-requisitos

- Docker Desktop instalado
- Docker Compose instalado
- 8GB+ de RAM disponível
- 10GB+ de espaço em disco

## 🚀 Build Automático

### Windows
```bash
# Execute o script
build-docker-images.bat
```

### Linux/Mac
```bash
# Tornar executável
chmod +x build-docker-images.sh

# Executar o script
./build-docker-images.sh
```

## 🔨 Build Manual

### 1. Build do Backend
```bash
# Navegar para o diretório do backend
cd backend

# Build da imagem
docker build -t milapp-backend:latest .

# Verificar se foi criada
docker images | grep milapp-backend
```

### 2. Build do Frontend
```bash
# Navegar para o diretório do frontend
cd frontend

# Build da imagem
docker build -t milapp-frontend:latest .

# Verificar se foi criada
docker images | grep milapp-frontend
```

### 3. Build Completo com Docker Compose
```bash
# Na raiz do projeto
docker-compose build

# Ou com no cache
docker-compose build --no-cache
```

## 📊 Verificação das Imagens

### Listar todas as imagens
```bash
docker images | grep milapp
```

### Verificar detalhes de uma imagem
```bash
# Backend
docker inspect milapp-backend:latest

# Frontend
docker inspect milapp-frontend:latest
```

### Verificar tamanho das imagens
```bash
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep milapp
```

## 🚀 Execução das Imagens

### Executar individualmente
```bash
# Backend
docker run -d -p 8000:8000 --name milapp-backend milapp-backend:latest

# Frontend
docker run -d -p 3000:80 --name milapp-frontend milapp-frontend:latest
```

### Executar com Docker Compose
```bash
# Subir todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar todos
docker-compose down
```

## 🔧 Configuração de Ambiente

### 1. Criar arquivo .env
```bash
cp env.example .env
```

### 2. Editar variáveis obrigatórias
```bash
# Backend
SECRET_KEY=your-secret-key-here
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

## 📈 Monitoramento

### Health Checks
```bash
# Frontend
curl http://localhost:3000/health

# Backend
curl http://localhost:8000/health

# Prometheus
curl http://localhost:9090/-/healthy
```

### Logs em tempo real
```bash
# Todos os serviços
docker-compose logs -f

# Serviço específico
docker-compose logs -f frontend
docker-compose logs -f backend
```

## 🐛 Troubleshooting

### Problemas comuns

#### 1. Erro de permissão
```bash
# Linux/Mac
sudo chown -R $USER:$USER .

# Windows
# Executar como administrador
```

#### 2. Porta já em uso
```bash
# Verificar portas
netstat -tulpn | grep :3000
netstat -tulpn | grep :8000

# Parar serviços conflitantes
sudo systemctl stop nginx  # se necessário
```

#### 3. Build falha
```bash
# Limpar cache
docker system prune -a

# Rebuild sem cache
docker-compose build --no-cache
```

#### 4. Container não inicia
```bash
# Verificar logs
docker-compose logs frontend
docker-compose logs backend

# Verificar configuração
docker-compose config
```

## 📋 Comandos Úteis

### Gerenciamento de imagens
```bash
# Listar imagens
docker images

# Remover imagem
docker rmi milapp-frontend:latest

# Remover todas as imagens não utilizadas
docker image prune -a
```

### Gerenciamento de containers
```bash
# Listar containers
docker ps -a

# Parar container
docker stop milapp-frontend

# Remover container
docker rm milapp-frontend

# Executar comando no container
docker exec -it milapp-frontend sh
```

### Limpeza do sistema
```bash
# Limpar tudo
docker system prune -a

# Limpar volumes
docker volume prune

# Limpar redes
docker network prune
```

## 🌐 URLs de Acesso

Após execução bem-sucedida:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090
- **MinIO Console**: http://localhost:9001

## 📊 Métricas de Build

### Tamanhos esperados
- **milapp-backend**: ~500MB
- **milapp-frontend**: ~200MB
- **Total**: ~700MB

### Tempo de build
- **Backend**: 3-5 minutos
- **Frontend**: 2-3 minutos
- **Total**: 5-8 minutos

## 🎯 Conclusão

Com estes scripts e instruções, você pode:

1. ✅ **Build automático** - Scripts prontos
2. ✅ **Build manual** - Controle total
3. ✅ **Verificação** - Health checks
4. ✅ **Monitoramento** - Logs e métricas
5. ✅ **Troubleshooting** - Solução de problemas
6. ✅ **Limpeza** - Gerenciamento de recursos

**Status: ✅ PRONTO PARA PRODUÇÃO** 