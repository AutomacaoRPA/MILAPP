# 🚀 MILAPP - Center of Excellence in Automation

[![Build Status](https://github.com/medsenior/milapp/workflows/CI/badge.svg)](https://github.com/medsenior/milapp/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://hub.docker.com/r/medsenior/milapp)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Supabase](https://img.shields.io/badge/Supabase-Ready-orange.svg)](https://supabase.com)

> **MILAPP** é uma plataforma integrada para gerenciamento de Centers of Excellence (CoE) em Automação, combinando IA conversacional, gestão de projetos ágeis, governança de qualidade e dashboards executivos.

## 🎯 Visão Geral

O MILAPP revoluciona a gestão de CoEs de automação através de uma abordagem integrada que combina:

- 🤖 **IA Conversacional Multimodal** para coleta de requisitos
- 📋 **Gestão Ágil de Projetos** com metodologias Scrum/Kanban
- 🎯 **Governança de Qualidade** com gates e métricas
- 📊 **Dashboards Executivos** em tempo real
- 🔧 **Recomendação de Ferramentas RPA** inteligente
- 🔐 **Controle de Acesso RBAC** robusto

## ✨ Principais Funcionalidades

### 🤖 IA Conversacional Multimodal
- Processamento de texto, imagens, PDFs, áudio e BPMN
- Extração automática de requisitos
- Geração de user stories
- Recomendação inteligente de ferramentas RPA

### 📋 Gestão de Projetos Ágeis
- Boards Scrum/Kanban integrados
- Sprints e releases automatizados
- Métricas de velocidade e burndown
- Integração com ferramentas externas

### 🎯 Governança de Qualidade
- Quality Gates configuráveis
- Métricas de qualidade em tempo real
- Auditoria e compliance
- Relatórios executivos

### 📊 Dashboards Executivos
- KPIs em tempo real
- Gráficos interativos
- Filtros avançados
- Exportação de relatórios

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   React/Streamlit│◄──►│   FastAPI       │◄──►│   Supabase      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐             │
         └─────────────►│   Redis Cache   │◄────────────┘
                        └─────────────────┘
                                │
                        ┌─────────────────┐
                        │   AI Services   │
                        │  OpenAI/LangChain│
                        └─────────────────┘
```

## 🛠️ Stack Tecnológica

### Backend
- **FastAPI** - API REST moderna e rápida
- **SQLAlchemy** - ORM para PostgreSQL
- **Redis** - Cache e sessões
- **LangChain** - Framework de IA
- **OpenAI** - Modelos de linguagem

### Frontend
- **React 18** - Interface moderna
- **Material-UI** - Componentes elegantes
- **Streamlit** - Dashboards interativos
- **Chart.js** - Visualizações

### Infraestrutura
- **Docker** - Containerização
- **PostgreSQL** - Banco de dados principal
- **Supabase** - Backend-as-a-Service
- **Nginx** - Proxy reverso

## 📸 Screenshots

### Chat IA Multimodal
![Chat Interface](docs/images/chat-interface.png)

### Dashboards Executivos
![Dashboards](docs/images/dashboards.png)

### Gestão de Projetos
![Project Management](docs/images/project-management.png)

### Quality Gates
![Quality Gates](docs/images/quality-gates.png)

## 🎬 Demo

Acesse uma demonstração online em: https://milapp-demo.medsenior.com

**Credenciais de Demo:**
- **Usuário:** demo@medsenior.com
- **Senha:** demo123

## 🚀 Quick Start

### Pré-requisitos
- Docker e Docker Compose
- Git
- 4GB RAM disponível

### Instalação

```bash
# Clone o repositório
git clone https://github.com/medsenior/milapp.git
cd milapp

# Execute o setup automático
chmod +x setup.sh
./setup.sh
```

### Configuração

1. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

2. **Inicie os serviços:**
```bash
docker-compose up -d
```

3. **Acesse a aplicação:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Dashboards: http://localhost:8501
- Docs API: http://localhost:8000/docs

## � Documentação

### Guias de Uso
- [Guia de Início Rápido](docs/quick-start.md)
- [Configuração Avançada](docs/advanced-setup.md)
- [API Reference](docs/api-reference.md)
- [Deployment](docs/deployment.md)

### Arquitetura
- [Visão Geral da Arquitetura](docs/architecture.md)
- [Modelos de Dados](docs/data-models.md)
- [Integrações](docs/integrations.md)
- [Segurança](docs/security.md)

## 🔧 Desenvolvimento

### Estrutura do Projeto
```
milapp/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── services/       # Lógica de negócio
│   │   ├── api/           # Endpoints
│   │   └── core/          # Configurações
│   └── requirements.txt
├── frontend/               # React App
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── services/      # Serviços API
│   │   └── utils/         # Utilitários
│   └── package.json
├── dashboards/            # Streamlit Dashboards
│   ├── pages/            # Páginas do dashboard
│   └── requirements.txt
├── docker-compose.yml     # Orquestração
└── docs/                 # Documentação
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
streamlit run app.py
```

## 🧪 Testes

```bash
# Testes do Backend
cd backend
pytest

# Testes do Frontend
cd frontend
npm test

# Testes E2E
npm run test:e2e
```

## 📦 Deployment

### Docker
```bash
# Build das imagens
docker-compose build

# Deploy
docker-compose up -d
```

### Kubernetes
```bash
kubectl apply -f k8s/
```

### Cloud Platforms
- [Deploy no Heroku](docs/deployment/heroku.md)
- [Deploy no Railway](docs/deployment/railway.md)
- [Deploy no AWS](docs/deployment/aws.md)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Guidelines
- Siga o [Conventional Commits](https://conventionalcommits.org/)
- Mantenha a cobertura de testes acima de 80%
- Documente novas funcionalidades
- Atualize a documentação quando necessário

## 📊 Roadmap

### v1.1.0 (Q1 2024)
- [ ] Integração com Jira/Confluence
- [ ] Machine Learning para recomendação de ferramentas
- [ ] Mobile app nativo
- [ ] Integração com Azure DevOps

### v1.2.0 (Q2 2024)
- [ ] Analytics avançados
- [ ] IA para análise de código
- [ ] Integração com GitHub/GitLab
- [ ] Workflow automation

### v2.0.0 (Q3 2024)
- [ ] Multi-tenant architecture
- [ ] Marketplace de plugins
- [ ] API pública
- [ ] Integração com Salesforce

## 📈 Métricas

- **Performance:** < 200ms response time
- **Uptime:** 99.9% SLA
- **Test Coverage:** > 80%
- **Security:** OWASP Top 10 compliance

## 🏆 Casos de Uso

### Empresas de Consultoria
- Gestão de múltiplos projetos de automação
- Padronização de metodologias
- Relatórios executivos para clientes

### CoEs Internos
- Centralização de conhecimento
- Governança de qualidade
- Treinamento de equipes

### Startups de RPA
- MVP rápido para clientes
- Demonstração de capacidades
- Gestão de projetos piloto

## 🆘 Suporte

- **Documentação:** [docs.milapp.com](https://docs.milapp.com)
- **Issues:** [GitHub Issues](https://github.com/medsenior/milapp/issues)
- **Discord:** [Comunidade MILAPP](https://discord.gg/milapp)
- **Email:** support@medsenior.com

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/) pela excelente framework
- [React](https://reactjs.org/) pela interface moderna
- [Supabase](https://supabase.com/) pelo backend robusto
- [OpenAI](https://openai.com/) pelos modelos de IA
- [Material-UI](https://mui.com/) pelos componentes elegantes

---

**⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!**

**Made with ❤️ by the MILAPP Team**
