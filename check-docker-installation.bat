@echo off
REM Script para verificar instalação do Docker
REM MILAPP - Centro de Excelência em Automação RPA

echo 🐳 Verificação de Instalação do Docker
echo ======================================
echo.

REM Verificar se o Docker está instalado
echo 📋 Verificando Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker não está instalado!
    echo.
    echo 📥 Para instalar o Docker Desktop:
    echo    1. Acesse: https://www.docker.com/products/docker-desktop/
    echo    2. Baixe o Docker Desktop para Windows
    echo    3. Execute o instalador
    echo    4. Siga o guia: DOCKER_INSTALLATION_GUIDE.md
    echo.
    pause
    exit /b 1
)

echo ✅ Docker detectado:
docker --version

REM Verificar Docker Compose
echo.
echo 📋 Verificando Docker Compose...
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Docker Compose não encontrado, mas Docker está instalado
) else (
    echo ✅ Docker Compose detectado:
    docker-compose --version
)

REM Verificar se o Docker está rodando
echo.
echo 📋 Verificando se o Docker está rodando...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker não está rodando!
    echo.
    echo 🔄 Para iniciar o Docker:
    echo    1. Abra o Docker Desktop
    echo    2. Aguarde a inicialização
    echo    3. Execute este script novamente
    echo.
    pause
    exit /b 1
)

echo ✅ Docker está rodando!

REM Verificar WSL 2
echo.
echo 📋 Verificando WSL 2...
wsl --list --verbose >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ WSL 2 não encontrado
    echo.
    echo 📥 Para instalar WSL 2:
    echo    1. Abra PowerShell como Administrador
    echo    2. Execute: dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all
    echo    3. Execute: dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all
    echo    4. Reinicie o computador
    echo    5. Baixe o kernel: https://aka.ms/wsl2kernel
    echo.
) else (
    echo ✅ WSL 2 detectado:
    wsl --list --verbose
)

REM Testar Docker com hello-world
echo.
echo 📋 Testando Docker...
docker run --rm hello-world >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Teste do Docker falhou!
    echo.
    echo 🔧 Possíveis soluções:
    echo    1. Reinicie o Docker Desktop
    echo    2. Verifique se a virtualização está habilitada na BIOS
    echo    3. Verifique se o WSL 2 está funcionando
    echo.
) else (
    echo ✅ Teste do Docker passou!
)

REM Verificar recursos do sistema
echo.
echo 📋 Verificando recursos do sistema...
echo Memória RAM:
wmic computersystem get TotalPhysicalMemory /format:value | findstr "="

echo.
echo Espaço em disco:
wmic logicaldisk get size,freespace,caption /format:table

REM Verificar portas em uso
echo.
echo 📋 Verificando portas do projeto...
netstat -ano | findstr :3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️ Porta 3000 está em uso
) else (
    echo ✅ Porta 3000 disponível
)

netstat -ano | findstr :8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️ Porta 8000 está em uso
) else (
    echo ✅ Porta 8000 disponível
)

REM Verificar se o projeto está no diretório correto
echo.
echo 📋 Verificando projeto...
if exist "docker-compose.yml" (
    echo ✅ Projeto MILAPP encontrado
) else (
    echo ❌ Projeto MILAPP não encontrado!
    echo.
    echo 📁 Certifique-se de estar no diretório correto:
    echo    C:\Users\bruno.souza\Desktop\Automação de Processos\Nova pasta
    echo.
)

if exist ".env" (
    echo ✅ Arquivo .env encontrado
) else (
    echo ⚠️ Arquivo .env não encontrado
    echo.
    echo 📝 Para criar o arquivo .env:
    echo    copy env.example .env
    echo.
)

echo.
echo 🎉 Verificação concluída!
echo.
echo 📋 Próximos passos:
echo    1. Se tudo estiver ✅, execute: .\build-docker-images.bat
echo    2. Após o build, execute: docker-compose up -d
echo    3. Acesse: http://localhost:3000
echo.
echo 📚 Para mais informações, consulte:
echo    - DOCKER_INSTALLATION_GUIDE.md
echo    - BUILD_INSTRUCTIONS.md
echo.
pause 