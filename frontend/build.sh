#!/bin/bash

# Script de build para o Frontend do MILAPP

echo "🚀 Iniciando build do Frontend MILAPP..."

# Verificar se o Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale o Node.js 18+"
    exit 1
fi

# Verificar se o npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ npm não encontrado. Por favor, instale o npm"
    exit 1
fi

# Verificar versão do Node.js
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js versão 18+ é necessária. Versão atual: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detectado"

# Limpar cache do npm
echo "🧹 Limpando cache do npm..."
npm cache clean --force

# Remover node_modules e package-lock.json se existirem
if [ -d "node_modules" ]; then
    echo "🗑️ Removendo node_modules..."
    rm -rf node_modules
fi

if [ -f "package-lock.json" ]; then
    echo "🗑️ Removendo package-lock.json..."
    rm package-lock.json
fi

# Instalar dependências
echo "📦 Instalando dependências..."
npm install

# Verificar se a instalação foi bem-sucedida
if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

# Executar testes (se existirem)
if [ -f "package.json" ] && grep -q "\"test\":" package.json; then
    echo "🧪 Executando testes..."
    npm test -- --watchAll=false
fi

# Build da aplicação
echo "🔨 Executando build..."
npm run build

# Verificar se o build foi bem-sucedido
if [ $? -ne 0 ]; then
    echo "❌ Erro no build da aplicação"
    exit 1
fi

# Verificar se o diretório build foi criado
if [ ! -d "build" ]; then
    echo "❌ Diretório build não foi criado"
    exit 1
fi

echo "✅ Build concluído com sucesso!"
echo "📁 Arquivos gerados em: $(pwd)/build"
echo "🚀 Para executar: npm start"
echo "🐳 Para Docker: docker-compose up frontend" 