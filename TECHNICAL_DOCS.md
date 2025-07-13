# MILAPP - Documentação Técnica

## 📋 Índice
1. [Arquitetura do Sistema](#arquitetura)
2. [Stack Tecnológico](#stack)
3. [Estrutura de Dados](#dados)
4. [APIs e Endpoints](#apis)
5. [Integrações](#integrações)
6. [Deploy e Infraestrutura](#deploy)
7. [Segurança](#segurança)
8. [Monitoramento](#monitoramento)
9. [Desenvolvimento](#desenvolvimento)

---

## 🏗️ Arquitetura do Sistema {#arquitetura}

### Visão Geral
O MILAPP é uma aplicação web distribuída com arquitetura de microserviços, composta por:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Dashboards    │
│   (React)       │◄──►│   (FastAPI)     │◄──►│  (Streamlit)    │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 8501    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Database      │
                    │  (PostgreSQL)   │
                    │   Port: 5432    │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │     Cache       │
                    │    (Redis)      │
                    │   Port: 6379    │
                    └─────────────────┘
```

### Componentes Principais

#### 1. Frontend (React + TypeScript)
- **Tecnologia**: React 18 + TypeScript
- **UI Framework**: Material-UI (MUI)
- **Estado**: Redux Toolkit + Zustand
- **Roteamento**: React Router DOM
- **HTTP Client**: Axios
- **Build Tool**: Create React App

#### 2. Backend (FastAPI + Python)
- **Framework**: FastAPI
- **Linguagem**: Python 3.11
- **ORM**: SQLAlchemy 2.0
- **Validação**: Pydantic
- **IA/ML**: LangChain + OpenAI
- **Processamento**: OpenCV, PyPDF2, Whisper

#### 3. Database (PostgreSQL)
- **SGBD**: PostgreSQL 15
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Backup**: Automático via Docker

#### 4. Cache (Redis)
- **Sessões**: Armazenamento de sessões
- **Cache**: Cache de consultas
- **Filas**: Processamento assíncrono

#### 5. Dashboards (Streamlit)
- **Framework**: Streamlit
- **Visualização**: Plotly
- **Dados**: Pandas + NumPy

---

## 🛠️ Stack Tecnológico {#stack}

### Backend
```python
# Dependências principais
fastapi==0.104.1          # Framework web
uvicorn[standard]==0.24.0  # ASGI server
sqlalchemy==2.0.23         # ORM
pydantic==2.5.0           # Validação de dados
openai==1.3.7             # OpenAI API
langchain==0.0.350        # Framework de IA
redis==5.0.1              # Cache
psycopg2-binary==2.9.9    # PostgreSQL driver
```

### Frontend
```json
{
  "react": "^18.2.0",
  "@mui/material": "^5.14.20",
  "@mui/icons-material": "^5.14.19",
  "axios": "^1.6.2",
  "react-router-dom": "^6.20.1",
  "react-query": "^3.39.3",
  "zustand": "^4.4.7"
}
```

### Infraestrutura
```yaml
# Docker Compose
version: '3.8'
services:
  - backend (FastAPI)
  - frontend (React)
  - dashboards (Streamlit)
  - postgres (Database)
  - redis (Cache)
  - nginx (Proxy)
```

---

## 🗄️ Estrutura de Dados {#dados}

### Modelo de Dados Principal

#### Tabela: users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'stakeholder',
    azure_id VARCHAR(255) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    department VARCHAR(100),
    position VARCHAR(100),
    phone VARCHAR(20),
    avatar_url VARCHAR(500),
    email_notifications BOOLEAN DEFAULT TRUE,
    teams_notifications BOOLEAN DEFAULT TRUE,
    whatsapp_notifications BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

#### Tabela: projects
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'planning',
    methodology VARCHAR(50) DEFAULT 'scrum',
    created_by UUID REFERENCES users(id),
    team_id UUID REFERENCES teams(id),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    settings JSONB DEFAULT '{}',
    estimated_hours INTEGER DEFAULT 0,
    actual_hours INTEGER DEFAULT 0,
    budget INTEGER DEFAULT 0,
    actual_cost INTEGER DEFAULT 0,
    quality_score INTEGER DEFAULT 0,
    risk_level VARCHAR(20) DEFAULT 'low',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Tabela: conversations
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    user_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    ai_summary TEXT,
    extracted_requirements JSONB DEFAULT '[]',
    confidence_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

#### Tabela: messages
```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    type VARCHAR(50) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT,
    file_path VARCHAR(500),
    file_size INTEGER,
    file_type VARCHAR(100),
    ai_analysis JSONB DEFAULT '{}',
    tokens_used INTEGER DEFAULT 0,
    processing_time INTEGER DEFAULT 0,
    is_processed BOOLEAN DEFAULT FALSE,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Relacionamentos
- **Users** 1:N **Projects** (um usuário pode ter vários projetos)
- **Projects** 1:N **Conversations** (um projeto pode ter várias conversas)
- **Conversations** 1:N **Messages** (uma conversa pode ter várias mensagens)
- **Projects** 1:N **User Stories** (um projeto pode ter várias user stories)
- **Projects** 1:N **Quality Gates** (um projeto passa por vários gates)

---

## 🔌 APIs e Endpoints {#apis}

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints Principais

#### Conversações (Módulo 1 - IA)
```http
POST   /conversations/                    # Criar conversação
GET    /conversations/                    # Listar conversações
GET    /conversations/{id}                # Obter conversação
PUT    /conversations/{id}                # Atualizar conversação
DELETE /conversations/{id}                # Deletar conversação

POST   /conversations/{id}/messages       # Enviar mensagem
GET    /conversations/{id}/messages       # Listar mensagens

POST   /conversations/{id}/extract-requirements    # Extrair requisitos
POST   /conversations/{id}/generate-user-stories   # Gerar user stories
POST   /conversations/{id}/recommend-tool          # Recomendar ferramenta
```

#### Projetos (Módulo 3 - Ágil)
```http
POST   /projects/                         # Criar projeto
GET    /projects/                         # Listar projetos
GET    /projects/{id}                     # Obter projeto
PUT    /projects/{id}                     # Atualizar projeto
DELETE /projects/{id}                     # Deletar projeto

GET    /projects/{id}/sprints             # Listar sprints
POST   /projects/{id}/sprints             # Criar sprint
GET    /projects/{id}/user-stories        # Listar user stories
POST   /projects/{id}/user-stories        # Criar user story
```

#### Quality Gates (Módulo 4 - Governança)
```http
GET    /quality-gates/                    # Listar quality gates
POST   /quality-gates/                    # Criar quality gate
GET    /quality-gates/{id}                # Obter quality gate
PUT    /quality-gates/{id}                # Atualizar quality gate
POST   /quality-gates/{id}/approve        # Aprovar quality gate
```

### Exemplo de Uso

#### Criar Conversação
```bash
curl -X POST "http://localhost:8000/api/v1/conversations/" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Automação de Processo de RH"
  }'
```

#### Enviar Mensagem
```bash
curl -X POST "http://localhost:8000/api/v1/conversations/123/messages" \
  -F "message_type=text" \
  -F "content=Preciso automatizar o processo de onboarding de funcionários"
```

#### Extrair Requisitos
```bash
curl -X POST "http://localhost:8000/api/v1/conversations/123/extract-requirements"
```

---

## 🔗 Integrações {#integrações}

### 1. OpenAI Integration
```python
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Processamento de texto
response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[{"role": "user", "content": "Analise este processo..."}]
)

# Transcrição de áudio
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)
```

### 2. Supabase Integration
```python
from supabase import create_client

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Inserir dados
data = supabase.table('conversations').insert({
    'project_id': project_id,
    'title': title
}).execute()

# Consultar dados
response = supabase.table('conversations').select('*').execute()
```

### 3. Azure AD Integration
```python
from azure.identity import ClientSecretCredential
from azure.graphrbac import GraphRbacManagementClient

credential = ClientSecretCredential(
    tenant_id=settings.AZURE_TENANT_ID,
    client_id=settings.AZURE_CLIENT_ID,
    client_secret=settings.AZURE_CLIENT_SECRET
)

client = GraphRbacManagementClient(credential, settings.AZURE_TENANT_ID)
```

### 4. Teams Integration
```python
import requests

def send_teams_notification(message: str, webhook_url: str):
    payload = {
        "text": message,
        "type": "message"
    }
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 200
```

### 5. WhatsApp Integration
```python
import requests

def send_whatsapp_message(phone: str, message: str):
    url = "https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code == 200
```

---

## 🚀 Deploy e Infraestrutura {#deploy}

### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://milapp:milapp123@postgres:5432/milapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=milapp
      - POSTGRES_USER=milapp
      - POSTGRES_PASSWORD=milapp123
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
```

### Variáveis de Ambiente
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/milapp
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# AI Services
OPENAI_API_KEY=sk-your-openai-key
LANGCHAIN_API_KEY=your-langchain-key

# Azure Integration
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret

# Notifications
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...
WHATSAPP_API_KEY=your-whatsapp-key
```

### Comandos de Deploy
```bash
# Setup inicial
./setup.sh

# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Ver logs
docker-compose logs -f

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

---

## 🔒 Segurança {#segurança}

### Autenticação e Autorização
```python
# JWT Token
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

### RBAC (Role-Based Access Control)
```python
ROLES = {
    "admin": {
        "permissions": ["*"]  # Todas as permissões
    },
    "architect": {
        "permissions": [
            "projects.*",
            "conversations.*",
            "documents.*",
            "quality_gates.*"
        ]
    },
    "po": {
        "permissions": [
            "projects.*",
            "conversations.*",
            "user_stories.*"
        ]
    },
    "developer": {
        "permissions": [
            "projects.read",
            "user_stories.*",
            "code_artifacts.*"
        ]
    }
}
```

### Validação de Dados
```python
from pydantic import BaseModel, validator

class MessageCreate(BaseModel):
    type: str
    content: Optional[str] = None
    file_path: Optional[str] = None
    
    @validator('type')
    def validate_type(cls, v):
        if v not in ['text', 'image', 'pdf', 'audio', 'bpmn']:
            raise ValueError('Tipo de mensagem inválido')
        return v
```

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Monitoramento {#monitoramento}

### Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": settings.APP_VERSION,
        "services": {
            "database": check_database(),
            "redis": check_redis(),
            "openai": check_openai()
        }
    }
```

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/milapp.log'),
        logging.StreamHandler()
    ]
)
```

### Métricas
```python
from prometheus_client import Counter, Histogram, generate_latest

# Métricas
requests_total = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    requests_total.inc()
    request_duration.observe(duration)
    
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

---

## 👨‍💻 Desenvolvimento {#desenvolvimento}

### Setup de Desenvolvimento
```bash
# Clone o repositório
git clone https://github.com/medsenior/milapp.git
cd milapp

# Configure o ambiente
cp .env.example .env
# Edite .env com suas configurações

# Execute o setup
./setup.sh
```

### Estrutura de Desenvolvimento
```
milapp/
├── backend/                 # Backend FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints da API
│   │   ├── core/           # Configurações
│   │   ├── models/         # Modelos de dados
│   │   ├── services/       # Serviços de negócio
│   │   └── main.py         # Aplicação principal
│   ├── requirements.txt     # Dependências Python
│   └── Dockerfile          # Container do backend
├── frontend/               # Frontend React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── pages/          # Páginas
│   │   ├── services/       # Serviços de API
│   │   └── App.tsx         # Aplicação principal
│   ├── package.json        # Dependências Node.js
│   └── Dockerfile          # Container do frontend
├── dashboards/             # Dashboards Streamlit
│   ├── streamlit_app.py    # Aplicação Streamlit
│   ├── requirements.txt     # Dependências Python
│   └── Dockerfile          # Container dos dashboards
├── docker-compose.yml      # Orquestração Docker
├── setup.sh               # Script de setup
└── README.md              # Documentação
```

### Comandos de Desenvolvimento
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm start

# Dashboards
cd dashboards
pip install -r requirements.txt
streamlit run streamlit_app.py

# Testes
pytest backend/tests/
npm test frontend/
```

### Code Style
```python
# Python (Black + isort)
black backend/
isort backend/

# TypeScript (ESLint + Prettier)
npm run lint
npm run format
```

---

## 📈 Roadmap

### Fase 1 (Atual) - MVP
- [x] Chat IA multimodal
- [x] Processamento de documentos
- [x] Extração de requisitos
- [x] Interface básica

### Fase 2 (Q2 2024) - Funcionalidades Avançadas
- [ ] Quality Gates completos
- [ ] Sistema de aprovações
- [ ] Dashboards executivos
- [ ] Integração com Azure DevOps

### Fase 3 (Q3 2024) - Automação
- [ ] Pipeline CI/CD integrado
- [ ] Deploy automático
- [ ] Monitoramento avançado
- [ ] Alertas inteligentes

### Fase 4 (Q4 2024) - IA Avançada
- [ ] Análise preditiva
- [ ] Recomendações automáticas
- [ ] Otimização de processos
- [ ] Machine Learning customizado

---

## 🤝 Contribuição

### Como Contribuir
1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente suas mudanças
4. Adicione testes
5. Faça commit com mensagem descritiva
6. Abra um Pull Request

### Padrões de Código
- Python: PEP 8, Black, isort
- TypeScript: ESLint, Prettier
- Commits: Conventional Commits
- Documentação: Docstrings, README atualizado

### Testes
```bash
# Backend
pytest backend/tests/ -v

# Frontend
npm test -- --coverage

# E2E
npm run test:e2e
```

---

*Esta documentação técnica é atualizada regularmente conforme o desenvolvimento do MILAPP.*