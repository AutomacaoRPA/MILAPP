# 🐳 Guia de Instalação do Docker - Windows

## 📋 Pré-requisitos

### Sistema Operacional
- ✅ Windows 10/11 (64-bit)
- ✅ Windows Server 2016 ou superior
- ✅ WSL 2 (Windows Subsystem for Linux 2)

### Requisitos de Hardware
- ✅ 4GB+ de RAM (8GB recomendado)
- ✅ 10GB+ de espaço em disco
- ✅ Processador com suporte a virtualização

## 🚀 Instalação Passo a Passo

### 1. Verificar Suporte à Virtualização

#### Verificar se a virtualização está habilitada:
```powershell
# Abrir PowerShell como Administrador
systeminfo
```

Procure por:
- **Virtualização habilitada na BIOS**: Sim
- **Hyper-V**: Sim

#### Se não estiver habilitado:
1. Reinicie o computador
2. Entre na BIOS (F2, F10, Del - depende da placa)
3. Procure por "Virtualization Technology", "Intel VT-x", "AMD-V"
4. Habilite e salve
5. Reinicie

### 2. Instalar WSL 2

#### Abrir PowerShell como Administrador:
```powershell
# Habilitar recurso WSL
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Habilitar recurso de Máquina Virtual
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Reiniciar o computador
shutdown /r /t 0
```

#### Após reiniciar, baixar e instalar o kernel do Linux:
1. Acesse: https://aka.ms/wsl2kernel
2. Baixe e instale o pacote
3. Defina WSL 2 como padrão:
```powershell
wsl --set-default-version 2
```

### 3. Instalar Docker Desktop

#### Baixar Docker Desktop:
1. Acesse: https://www.docker.com/products/docker-desktop/
2. Clique em "Download for Windows"
3. Execute o instalador baixado

#### Durante a instalação:
- ✅ Marque "Use WSL 2 instead of Hyper-V"
- ✅ Marque "Add shortcut to desktop"
- ✅ Marque "Use the WSL 2 based engine"

#### Após instalação:
1. Reinicie o computador
2. Abra o Docker Desktop
3. Aguarde a inicialização (pode demorar alguns minutos)

### 4. Verificar Instalação

#### Abrir PowerShell ou Command Prompt:
```powershell
# Verificar versão do Docker
docker --version

# Verificar versão do Docker Compose
docker-compose --version

# Testar instalação
docker run hello-world
```

### 5. Configurações Recomendadas

#### Abrir Docker Desktop:
1. Clique no ícone do Docker na bandeja do sistema
2. Vá em Settings (⚙️)
3. Configure:

#### **Resources:**
- **Memory**: 6GB (ou metade da RAM disponível)
- **CPUs**: 2 (ou metade dos cores disponíveis)
- **Disk image size**: 64GB

#### **Docker Engine:**
```json
{
  "registry-mirrors": [],
  "insecure-registries": [],
  "debug": false,
  "experimental": false,
  "features": {
    "buildkit": true
  }
}
```

## 🔧 Configuração do Projeto MILAPP

### 1. Clonar o Repositório
```powershell
# Navegar para o diretório desejado
cd "C:\Users\bruno.souza\Desktop\Automação de Processos\Nova pasta"

# Verificar se está no diretório correto
dir
```

### 2. Configurar Variáveis de Ambiente
```powershell
# Copiar arquivo de exemplo
copy env.example .env

# Editar o arquivo .env
notepad .env
```

### 3. Executar Build das Imagens
```powershell
# Executar script de build
.\build-docker-images.bat
```

### 4. Executar Aplicação
```powershell
# Subir todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## 🐛 Troubleshooting

### Problema: "Docker Desktop is starting..."
**Solução:**
1. Aguarde alguns minutos
2. Reinicie o Docker Desktop
3. Verifique se o WSL 2 está funcionando:
```powershell
wsl --list --verbose
```

### Problema: "WSL 2 installation is incomplete"
**Solução:**
```powershell
# Atualizar WSL
wsl --update

# Reiniciar WSL
wsl --shutdown
```

### Problema: "Virtualization is not enabled"
**Solução:**
1. Reinicie o computador
2. Entre na BIOS
3. Habilite "Virtualization Technology"
4. Salve e reinicie

### Problema: "Port already in use"
**Solução:**
```powershell
# Verificar portas em uso
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Parar processo se necessário
taskkill /PID <PID> /F
```

### Problema: "Permission denied"
**Solução:**
1. Execute PowerShell como Administrador
2. Ou adicione seu usuário ao grupo "docker-users"

## 📊 Verificação de Performance

### Verificar uso de recursos:
```powershell
# Ver containers em execução
docker ps

# Ver uso de recursos
docker stats

# Ver imagens
docker images
```

### Testar conectividade:
```powershell
# Testar frontend
curl http://localhost:3000

# Testar backend
curl http://localhost:8000/health
```

## 🎯 URLs de Acesso

Após execução bem-sucedida:

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001
- **Prometheus**: http://localhost:9090

## 📋 Comandos Úteis

### Gerenciamento básico:
```powershell
# Parar todos os containers
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Rebuild sem cache
docker-compose build --no-cache

# Ver logs de um serviço específico
docker-compose logs -f frontend
docker-compose logs -f backend
```

### Limpeza do sistema:
```powershell
# Remover containers parados
docker container prune

# Remover imagens não utilizadas
docker image prune

# Remover volumes não utilizados
docker volume prune

# Limpeza completa
docker system prune -a
```

## 🔒 Segurança

### Boas práticas:
1. ✅ Sempre execute como usuário normal (não admin)
2. ✅ Mantenha o Docker Desktop atualizado
3. ✅ Use imagens oficiais quando possível
4. ✅ Configure limites de recursos
5. ✅ Monitore logs regularmente

## 📞 Suporte

### Se precisar de ajuda:
1. **Documentação oficial**: https://docs.docker.com/
2. **Comunidade**: https://forums.docker.com/
3. **GitHub Issues**: Para problemas específicos do projeto

### Logs úteis:
```powershell
# Logs do Docker Desktop
Get-EventLog -LogName Application -Source "Docker Desktop"

# Logs do WSL
wsl --list --verbose
```

## 🎉 Conclusão

Após seguir este guia, você terá:
- ✅ Docker Desktop instalado e configurado
- ✅ WSL 2 funcionando
- ✅ Projeto MILAPP pronto para execução
- ✅ Monitoramento e logs configurados

**Status: ✅ PRONTO PARA USO** 