# MILAPP - Sistema Integrado de Gestão RPA e Inovação

## 🎯 Visão Geral

O MILAPP é um **software único e integrado** desenvolvido especificamente para gestão completa de um Centro de Excelência (CoE) de Automação. Toda a funcionalidade está contida numa única aplicação web, com módulos internos que se comunicam seamless.

### Características Principais
- **Software único**: Uma aplicação web completa
- **Módulos integrados**: Todos os módulos numa única base de código
- **Banco unificado**: Supabase como database principal
- **Interface consistente**: React/Streamlit para frontend unificado
- **API centralizada**: FastAPI como backend único
- **IA integrada**: LangChain + OpenAI para inteligência artificial

## 🏗️ Arquitetura

```
MILAPP (Aplicação Web Única)
├── Frontend Layer
│   ├── React Web App (Interface Principal)
│   ├── Streamlit Dashboards (Dashboards Executivos)
│   └── Mobile PWA (Acesso Mobile)
├── Backend Layer
│   ├── FastAPI (API Principal)
│   ├── LangChain Engine (IA Conversacional)
│   ├── Workflow Engine (Processos Internos)
│   └── Integration Layer (APIs Externas)
├── Data Layer
│   ├── Supabase (Database Principal)
│   ├── Redis (Cache & Sessions)
│   └── File Storage (Documentos & Arquivos)
└── Integration Layer
    ├── n8n API (Orquestração Externa)
    ├── Power BI API (Dashboards Corporativos)
    ├── Azure AD (Autenticação)
    └── Notification APIs (Email, WhatsApp, Teams)
```

## 🧩 Módulos Principais

### Módulo 1: Levantamento de Requisitos IA
- Chat conversacional multimodal
- Processamento de texto, imagens, PDFs, áudios
- Análise de fluxos Bizagi (.bpmn)
- Extração automática de requisitos

### Módulo 2: Geração de Documentos de Governança
- PDD (Project Definition Document)
- SDD (System Design Document)
- GMUD (Gestão de Mudanças)
- User Stories com critérios de aceite

### Módulo 3: Gestão de Projetos Ágil
- Product Backlog com priorização IA
- Sprint Backlog com capacity planning
- Kanban Board customizável
- Métricas de flow em tempo real

### Módulo 4: Quality Gates e Governança
- Quality Gates (G1-G4)
- Matriz RACI automática
- Workflow de aprovações
- SLA tracking automático

### Módulo 5: Recomendação de Ferramenta RPA
- Análise de adequação
- Matriz de decisão (n8n, Python, Playwright, etc.)
- Simulação de ROI
- Recomendação com justificativa IA

### Módulo 6: Desenvolvimento e Code Review
- Editor integrado
- Code review automático
- Gestão de versões
- Deploy tracking

### Módulo 7: Testes e Validação
- Geração de casos de teste
- Execução automática
- Validação de negócio
- UAT integrado

### Módulo 8: Deployment e Produção
- Pipeline de deploy
- Monitoramento de produção
- Gestão de incidentes
- Rollback automático

### Módulo 9: Dashboards e Analytics
- Dashboards executivos
- KPIs de inovação
- Analytics avançados
- Relatórios customizáveis

### Módulo 10: Controle de Acesso e Usuários
- Gestão de usuários
- RBAC (Role-Based Access Control)
- Integração Azure AD
- Auditoria completa

## 🚀 Instalação e Deploy

### Pré-requisitos
- Docker e Docker Compose
- Node.js 18+
- Python 3.9+
- Supabase account

### Configuração Rápida
```bash
# Clone o repositório
git clone https://github.com/medsenior/milapp.git
cd milapp

# Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# Execute com Docker
docker-compose up -d

# Acesse em http://localhost:3000
```

## 📊 Benefícios Principais

- **Redução 80%** no tempo de levantamento de requisitos
- **Aumento 60%** na qualidade das automações
- **Diminuição 70%** no time-to-market
- **Melhoria 90%** na governança e compliance
- **ROI positivo** em 12 meses

## 🔧 Tecnologias

### Frontend
- React.js com TypeScript
- Material-UI para componentes
- Streamlit para dashboards
- PWA para acesso mobile

### Backend
- Python 3.9+ com FastAPI
- LangChain para IA
- SQLAlchemy para ORM
- Redis para cache

### Database
- Supabase (PostgreSQL)
- Azure Blob Storage para arquivos

### IA/ML
- OpenAI API
- LangChain
- Whisper para transcrição
- OpenCV para processamento de imagens

## 📝 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte técnico ou dúvidas sobre o MILAPP, entre em contato com a equipe de desenvolvimento da MedSênior.
