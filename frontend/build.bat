@echo off
REM Script de build para o Frontend do MILAPP (Windows)

echo 🚀 Iniciando build do Frontend MILAPP...

REM Verificar se o Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js não encontrado. Por favor, instale o Node.js 18+
    pause
    exit /b 1
)

REM Verificar se o npm está instalado
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm não encontrado. Por favor, instale o npm
    pause
    exit /b 1
)

echo ✅ Node.js detectado

REM Limpar cache do npm
echo 🧹 Limpando cache do npm...
npm cache clean --force

REM Remover node_modules e package-lock.json se existirem
if exist "node_modules" (
    echo 🗑️ Removendo node_modules...
    rmdir /s /q node_modules
)

if exist "package-lock.json" (
    echo 🗑️ Removendo package-lock.json...
    del package-lock.json
)

REM Instalar dependências
echo 📦 Instalando dependências...
npm install

REM Verificar se a instalação foi bem-sucedida
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências
    pause
    exit /b 1
)

REM Executar testes (se existirem)
findstr /c:"\"test\":" package.json >nul
if %errorlevel% equ 0 (
    echo 🧪 Executando testes...
    npm test -- --watchAll=false
)

REM Build da aplicação
echo 🔨 Executando build...
npm run build

REM Verificar se o build foi bem-sucedido
if %errorlevel% neq 0 (
    echo ❌ Erro no build da aplicação
    pause
    exit /b 1
)

REM Verificar se o diretório build foi criado
if not exist "build" (
    echo ❌ Diretório build não foi criado
    pause
    exit /b 1
)

echo ✅ Build concluído com sucesso!
echo 📁 Arquivos gerados em: %cd%\build
echo 🚀 Para executar: npm start
echo 🐳 Para Docker: docker-compose up frontend
pause 