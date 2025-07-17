# MILAPP - Centro de Excelência em Automação RPA

## 🎯 Visão Geral

O MILAPP é uma plataforma única e integrada para gestão completa de Centros de Excelência (CoE) de Automação RPA. Desenvolvido especificamente para substituir múltiplas ferramentas externas, oferece uma solução autossuficiente com IA integrada, governança robusta e experiência unificada.

## 🏗️ Arquitetura

### Stack Tecnológico
- **Backend**: Python 3.11+ / FastAPI
- **Frontend**: React 18 / TypeScript / Material-UI
- **Database**: Supabase (PostgreSQL)
- **Cache**: Redis
- **IA**: OpenAI GPT-4 / LangChain
- **Containerização**: Docker / Docker Compose
- **Monitoramento**: Prometheus / Grafana

### Componentes Principais
- **Chat IA Multimodal**: Levantamento inteligente de requisitos
- **Gestão de Projetos Ágil**: Kanban nativo integrado
- **Quality Gates**: Governança automatizada (G1-G4)
- **Recomendação RPA**: Análise inteligente de ferramentas
- **Dashboards Executivos**: Analytics preditivos
- **Pipeline CI/CD**: Deploy automatizado

## 🚀 Configuração Rápida

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Docker e Docker Compose
- Conta no Supabase

### 1. Configuração do Supabase

1. **Crie um projeto no Supabase**:
   - Acesse [supabase.com](https://supabase.com)
   - Crie um novo projeto
   - Anote as credenciais: URL, anon key, service key

2. **Configure as variáveis de ambiente**:
   ```bash
   cp env.example .env
   ```

3. **Edite o arquivo `.env`**:
   ```env
   # Supabase Configuration (Required)
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-anon-key
   SUPABASE_SERVICE_KEY=your-service-key
   
   # Database Configuration (Optional - will use Supabase if not provided)
   DATABASE_URL=postgresql://user:password@localhost:5432/milapp
   
   # Redis Configuration
   REDIS_URL=redis://localhost:6379/0
   
   # Security
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # AI Services
   OPENAI_API_KEY=sk-your-openai-key
   LANGCHAIN_API_KEY=your-langchain-key
   
   # Azure AD Configuration (Optional)
   AZURE_TENANT_ID=your-tenant-id
   AZURE_CLIENT_ID=your-client-id
   AZURE_CLIENT_SECRET=your-client-secret
   ```

### 2. Instalação do Backend

```bash
cd backend

# Instalar dependências
pip install -r requirements.txt

# Configurar banco de dados
python -c "from app.core.database import init_db; init_db()"

# Executar aplicação
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Instalação do Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Executar aplicação
npm start
```

### 4. Execução com Docker

```bash
# Construir e executar todos os serviços
docker-compose up --build

# Acessar aplicação
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

## 📊 Estrutura do Projeto

```
milapp/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints da API
│   │   ├── core/           # Configurações centrais
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── services/       # Lógica de negócio
│   │   └── main.py         # Aplicação principal
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Aplicação React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── pages/          # Páginas da aplicação
│   │   ├── services/       # Serviços de API
│   │   └── styles/         # Estilos CSS
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml      # Orquestração Docker
├── env.example            # Variáveis de ambiente
└── README.md
```

## 🔧 Configuração do Supabase

### 1. Configuração do Banco de Dados

O MILAPP usa o Supabase como banco de dados principal. As tabelas são criadas automaticamente quando você executa:

```python
from app.core.database import init_db
init_db()
```

### 2. Estrutura das Tabelas

As principais tabelas incluem:
- `users`: Usuários do sistema
- `projects`: Projetos de automação
- `conversations`: Conversas com IA
- `messages`: Mensagens das conversas
- `documents`: Documentos gerados
- `tickets`: Tickets/User Stories
- `quality_gates`: Gates de qualidade
- `deployments`: Deployments de automações

### 3. Configuração de Segurança

Configure as políticas de segurança no Supabase:
- Row Level Security (RLS)
- Políticas de acesso por usuário
- Auditoria de ações

## 🎨 Design System

O MILAPP utiliza um design system unificado com:
- **Paleta de Cores**: Azul corporativo com tons neutros
- **Tipografia**: Inter para interface moderna
- **Componentes**: Material-UI com customizações
- **Responsividade**: Mobile-first design
- **Acessibilidade**: WCAG 2.1 AA compliance

## 🔐 Segurança

### Autenticação
- **Azure AD**: Integração SSO corporativa
- **JWT Tokens**: Autenticação stateless
- **MFA**: Autenticação multifator
- **RBAC**: Controle de acesso baseado em roles

### Dados
- **Criptografia**: AES-256 para dados sensíveis
- **Auditoria**: Log completo de ações
- **Backup**: Backup automático diário
- **Compliance**: GDPR, LGPD, SOX

## 📈 Monitoramento

### Métricas
- **Performance**: Tempo de resposta, throughput
- **Negócio**: ROI, produtividade, qualidade
- **Técnico**: Uptime, erros, recursos
- **Usuário**: Engajamento, satisfação

### Alertas
- **Críticos**: Falhas de sistema, downtime
- **Importantes**: Performance degradada
- **Informativos**: Novos usuários, projetos

## 🚀 Deploy

### Desenvolvimento
```bash
docker-compose up --build
```

### Produção
```bash
# Usando Kubernetes
kubectl apply -f k8s/

# Usando Docker Swarm
docker stack deploy -c docker-compose.prod.yml milapp
```

## 📚 Documentação

- **API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Guia do Usuário**: `/docs/user-guide/`
- **Documentação Técnica**: `/docs/technical/`
- **Troubleshooting**: `/docs/troubleshooting/`

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto é proprietário e confidencial.

## 🆘 Suporte

- **Email**: suporte@milapp.com
- **Documentação**: [docs.milapp.com](https://docs.milapp.com)
- **Issues**: GitHub Issues

---

**MILAPP - Transformando a Gestão de Automação Corporativa** 