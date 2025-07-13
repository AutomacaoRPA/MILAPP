#!/bin/bash

# MILAPP - Script de Setup
# Sistema Integrado de Gestão RPA e Inovação

set -e

echo "🚀 MILAPP - Setup Inicial"
echo "=========================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verifica se Docker está instalado
check_docker() {
    log "Verificando Docker..."
    if ! command -v docker &> /dev/null; then
        error "Docker não está instalado. Por favor, instale o Docker primeiro."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
        exit 1
    fi
    
    log "Docker e Docker Compose encontrados ✓"
}

# Verifica se arquivo .env existe
check_env() {
    log "Verificando arquivo de configuração..."
    if [ ! -f .env ]; then
        warn "Arquivo .env não encontrado. Criando a partir do exemplo..."
        cp .env.example .env
        log "Arquivo .env criado. Por favor, edite as variáveis de ambiente conforme necessário."
        echo ""
        echo "⚠️  IMPORTANTE: Edite o arquivo .env com suas configurações antes de continuar!"
        echo "   - Configure as chaves da OpenAI"
        echo "   - Configure as credenciais do Supabase"
        echo "   - Configure as integrações do Azure"
        echo ""
        read -p "Pressione Enter após editar o arquivo .env..."
    else
        log "Arquivo .env encontrado ✓"
    fi
}

# Cria diretórios necessários
create_directories() {
    log "Criando diretórios necessários..."
    mkdir -p uploads logs static
    log "Diretórios criados ✓"
}

# Verifica dependências do sistema
check_system_deps() {
    log "Verificando dependências do sistema..."
    
    # Verifica se git está instalado
    if ! command -v git &> /dev/null; then
        warn "Git não encontrado. Instalando..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y git
        elif command -v yum &> /dev/null; then
            sudo yum install -y git
        else
            error "Não foi possível instalar o Git automaticamente. Instale manualmente."
            exit 1
        fi
    fi
    
    log "Dependências do sistema verificadas ✓"
}

# Build das imagens Docker
build_images() {
    log "Construindo imagens Docker..."
    docker-compose build
    log "Imagens construídas ✓"
}

# Inicia os serviços
start_services() {
    log "Iniciando serviços..."
    docker-compose up -d
    log "Serviços iniciados ✓"
}

# Verifica se os serviços estão rodando
check_services() {
    log "Verificando status dos serviços..."
    
    # Aguarda um pouco para os serviços inicializarem
    sleep 10
    
    # Verifica backend
    if curl -f http://localhost:8000/health &> /dev/null; then
        log "Backend (FastAPI) ✓"
    else
        warn "Backend ainda não está respondendo. Aguarde alguns segundos..."
    fi
    
    # Verifica frontend
    if curl -f http://localhost:3000 &> /dev/null; then
        log "Frontend (React) ✓"
    else
        warn "Frontend ainda não está respondendo. Aguarde alguns segundos..."
    fi
    
    # Verifica dashboards
    if curl -f http://localhost:8501 &> /dev/null; then
        log "Dashboards (Streamlit) ✓"
    else
        warn "Dashboards ainda não estão respondendo. Aguarde alguns segundos..."
    fi
}

# Mostra informações finais
show_info() {
    echo ""
    echo "🎉 MILAPP instalado com sucesso!"
    echo "================================"
    echo ""
    echo "📱 Acesse as aplicações:"
    echo "   • Frontend:     http://localhost:3000"
    echo "   • Backend API:  http://localhost:8000"
    echo "   • Documentação: http://localhost:8000/docs"
    echo "   • Dashboards:   http://localhost:8501"
    echo ""
    echo "🔧 Comandos úteis:"
    echo "   • Parar serviços:    docker-compose down"
    echo "   • Ver logs:          docker-compose logs -f"
    echo "   • Reiniciar:         docker-compose restart"
    echo "   • Atualizar:         docker-compose pull && docker-compose up -d"
    echo ""
    echo "📚 Documentação:"
    echo "   • README.md - Documentação completa"
    echo "   • API Docs - http://localhost:8000/docs"
    echo ""
    echo "⚠️  Lembre-se de:"
    echo "   • Configurar as variáveis de ambiente no arquivo .env"
    echo "   • Configurar as integrações externas (OpenAI, Supabase, etc.)"
    echo "   • Testar todas as funcionalidades antes de usar em produção"
    echo ""
}

# Função principal
main() {
    echo ""
    log "Iniciando setup do MILAPP..."
    echo ""
    
    check_docker
    check_env
    create_directories
    check_system_deps
    build_images
    start_services
    check_services
    show_info
}

# Executa função principal
main "$@"