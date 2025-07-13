#!/bin/bash

# Script para inicializar o repositório Git e preparar para publicação
# Uso: ./scripts/init-repo.sh

set -e

echo "🚀 Inicializando repositório Git para MILAPP..."

# Verificar se estamos no diretório correto
if [ ! -f "README.md" ]; then
    echo "❌ Erro: Execute este script no diretório raiz do projeto"
    exit 1
fi

# Inicializar Git se não existir
if [ ! -d ".git" ]; then
    echo "📁 Inicializando repositório Git..."
    git init
fi

# Adicionar arquivo .gitignore se não existir
if [ ! -f ".gitignore" ]; then
    echo "📝 Criando .gitignore..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.yarn-integrity

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Docker
.dockerignore

# Database
*.db
*.sqlite3

# Cache
.cache/
.parcel-cache/

# Coverage
coverage/
.coverage
htmlcov/

# Temporary files
tmp/
temp/
EOF
fi

# Criar diretório docs/images se não existir
mkdir -p docs/images

# Criar arquivo de placeholder para screenshots
if [ ! -f "docs/images/chat-interface.png" ]; then
    echo "📸 Criando placeholders para screenshots..."
    echo "# Screenshot placeholder" > docs/images/chat-interface.png
    echo "# Screenshot placeholder" > docs/images/dashboards.png
    echo "# Screenshot placeholder" > docs/images/project-management.png
    echo "# Screenshot placeholder" > docs/images/quality-gates.png
fi

# Adicionar todos os arquivos
echo "📦 Adicionando arquivos ao Git..."
git add .

# Fazer commit inicial
echo "💾 Fazendo commit inicial..."
git commit -m "feat: Initial commit - MILAPP Center of Excellence in Automation

- Complete FastAPI backend with AI integration
- React frontend with Material-UI
- Streamlit dashboards
- Docker containerization
- Comprehensive documentation
- CI/CD pipeline setup

Features:
- AI conversational chat for requirements gathering
- Agile project management
- Quality gates and governance
- RPA tool recommendation
- Executive dashboards
- RBAC access control"

# Configurar branch main
if git branch --show-current 2>/dev/null | grep -q "main"; then
    echo "✅ Branch main já está ativa"
else
    echo "🔄 Renomeando branch para main..."
    git branch -M main
fi

# Configurar remote origin se não existir
if ! git remote get-url origin >/dev/null 2>&1; then
    echo "🔗 Configurando remote origin..."
    echo "Por favor, insira a URL do seu repositório GitHub:"
    read -p "URL do repositório (ex: https://github.com/medsenior/milapp.git): " repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote origin configurado: $repo_url"
    else
        echo "⚠️  Remote origin não configurado. Configure manualmente com:"
        echo "git remote add origin <URL_DO_SEU_REPOSITORIO>"
    fi
fi

# Criar arquivo CONTRIBUTING.md
if [ ! -f "CONTRIBUTING.md" ]; then
    echo "📝 Criando CONTRIBUTING.md..."
    cat > CONTRIBUTING.md << 'EOF'
# 🤝 Contribuindo para o MILAPP

Obrigado por considerar contribuir para o MILAPP! Este documento fornece diretrizes para contribuições.

## 🚀 Como Contribuir

### 1. Fork o Projeto
1. Acesse [https://github.com/medsenior/milapp](https://github.com/medsenior/milapp)
2. Clique em "Fork" no canto superior direito

### 2. Clone seu Fork
```bash
git clone https://github.com/seu-usuario/milapp.git
cd milapp
```

### 3. Configure o Ambiente
```bash
# Instalar dependências
./setup.sh

# Ou manualmente:
docker-compose up -d
```

### 4. Crie uma Branch
```bash
git checkout -b feature/nova-funcionalidade
```

### 5. Faça suas Alterações
- Escreva código limpo e bem documentado
- Adicione testes para novas funcionalidades
- Atualize a documentação quando necessário

### 6. Commit suas Alterações
```bash
git add .
git commit -m "feat: adiciona nova funcionalidade"
```

### 7. Push para seu Fork
```bash
git push origin feature/nova-funcionalidade
```

### 8. Abra um Pull Request
1. Vá para seu fork no GitHub
2. Clique em "New Pull Request"
3. Selecione a branch com suas alterações
4. Preencha o template do PR

## 📋 Diretrizes

### Código
- Siga as convenções de nomenclatura do projeto
- Mantenha a cobertura de testes acima de 80%
- Use Conventional Commits para mensagens de commit
- Documente funções e classes importantes

### Pull Requests
- Descreva claramente as mudanças
- Inclua testes quando aplicável
- Atualize a documentação se necessário
- Verifique se todos os testes passam

### Issues
- Use os templates fornecidos
- Forneça informações detalhadas
- Inclua screenshots quando relevante
- Verifique se não é um problema já reportado

## 🧪 Testes

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
```

### E2E
```bash
npm run test:e2e
```

## 📚 Recursos

- [Documentação](docs/)
- [API Reference](docs/api-reference.md)
- [Guia de Início Rápido](docs/quick-start.md)
- [Issues](https://github.com/medsenior/milapp/issues)

## 📞 Suporte

- **Discord:** [Comunidade MILAPP](https://discord.gg/milapp)
- **Email:** dev-support@medsenior.com
- **Issues:** [GitHub Issues](https://github.com/medsenior/milapp/issues)

## 🙏 Agradecimentos

Obrigado por contribuir para o MILAPP! 🚀
EOF
fi

# Criar arquivo CHANGELOG.md
if [ ! -f "CHANGELOG.md" ]; then
    echo "📝 Criando CHANGELOG.md..."
    cat > CHANGELOG.md << 'EOF'
# 📋 Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Added
- Sistema completo de gestão de CoE em automação
- IA conversacional multimodal para coleta de requisitos
- Gestão ágil de projetos com metodologias Scrum/Kanban
- Quality gates e governança de qualidade
- Recomendação inteligente de ferramentas RPA
- Dashboards executivos em tempo real
- Controle de acesso RBAC robusto
- API REST completa com FastAPI
- Frontend React com Material-UI
- Dashboards Streamlit interativos
- Containerização Docker completa
- Pipeline CI/CD com GitHub Actions
- Documentação técnica abrangente

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- Autenticação JWT implementada
- Controle de acesso baseado em roles
- Validação de entrada em todos os endpoints
- Sanitização de dados de entrada

## [1.0.0] - 2024-01-15

### Added
- Versão inicial do MILAPP
- Funcionalidades core implementadas
- Documentação completa
- Setup automatizado
EOF
fi

echo ""
echo "✅ Repositório inicializado com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure o remote origin:"
echo "   git remote add origin https://github.com/SEU_USUARIO/milapp.git"
echo ""
echo "2. Faça push para o GitHub:"
echo "   git push -u origin main"
echo ""
echo "3. Configure os secrets no GitHub:"
echo "   - DOCKER_USERNAME"
echo "   - DOCKER_PASSWORD"
echo "   - SNYK_TOKEN"
echo ""
echo "4. Ative o GitHub Actions no repositório"
echo ""
echo "5. Adicione screenshots reais em docs/images/"
echo ""
echo "🎉 Seu projeto está pronto para publicação!"