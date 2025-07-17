# 🚀 Instalação Rápida do Docker - Windows

## ⚡ Passos Rápidos

### 1. Baixar Docker Desktop
- **Link**: https://www.docker.com/products/docker-desktop/
- **Clique em**: "Download for Windows"
- **Tamanho**: ~500MB

### 2. Instalar
- **Execute** o arquivo baixado
- **Marque**: "Use WSL 2 instead of Hyper-V"
- **Marque**: "Add shortcut to desktop"
- **Clique**: Install

### 3. Reiniciar
- **Reinicie** o computador após a instalação
- **Abra** o Docker Desktop
- **Aguarde** a inicialização (2-5 minutos)

### 4. Verificar
```powershell
# Execute este comando
.\check-docker-installation.bat
```

## 🔧 Se Der Problema

### Problema: "WSL 2 installation is incomplete"
```powershell
# Abra PowerShell como Administrador
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all
shutdown /r /t 0
```

### Problema: "Virtualization is not enabled"
1. **Reinicie** o computador
2. **Entre na BIOS** (F2, F10, Del)
3. **Procure**: "Virtualization Technology", "Intel VT-x", "AMD-V"
4. **Habilite** e salve
5. **Reinicie**

### Problema: "Docker Desktop is starting..."
- **Aguarde** 5-10 minutos
- **Reinicie** o Docker Desktop
- **Verifique** se o WSL 2 está funcionando

## ✅ Após Instalação

### 1. Testar Instalação
```powershell
.\check-docker-installation.bat
```

### 2. Build das Imagens
```powershell
.\build-docker-images.bat
```

### 3. Executar Projeto
```powershell
docker-compose up -d
```

### 4. Acessar Aplicação
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000

## 📞 Suporte

### Se precisar de ajuda:
1. **Documentação oficial**: https://docs.docker.com/
2. **Comunidade**: https://forums.docker.com/
3. **Guia completo**: DOCKER_INSTALLATION_GUIDE.md

### Logs úteis:
```powershell
# Verificar se Docker está rodando
docker info

# Verificar WSL
wsl --list --verbose

# Verificar recursos
docker stats
```

## 🎯 Tempo Estimado

- **Download**: 5-10 minutos
- **Instalação**: 10-15 minutos
- **Configuração**: 5-10 minutos
- **Build do projeto**: 10-15 minutos
- **Total**: 30-50 minutos

## 🎉 Resultado Final

Após seguir estes passos, você terá:
- ✅ Docker Desktop funcionando
- ✅ Projeto MILAPP rodando
- ✅ Frontend e Backend acessíveis
- ✅ Monitoramento configurado

**Status: ✅ PRONTO PARA USO** 