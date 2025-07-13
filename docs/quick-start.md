# 🚀 Guia de Início Rápido - MILAPP

Este guia irá ajudá-lo a configurar e executar o MILAPP em menos de 10 minutos.

## 📋 Pré-requisitos

- **Docker** e **Docker Compose** instalados
- **Git** para clonar o repositório
- **4GB RAM** disponível
- **Conexão com internet** para download das imagens

## ⚡ Instalação Rápida

### 1. Clone o Repositório

```bash
git clone https://github.com/medsenior/milapp.git
cd milapp
```

### 2. Configure as Variáveis de Ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/milapp

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Redis
REDIS_URL=redis://localhost:6379
```

### 3. Execute o Setup Automático

```bash
chmod +x setup.sh
./setup.sh
```

Este script irá:
- Verificar os pré-requisitos
- Baixar as imagens Docker
- Configurar o banco de dados
- Iniciar todos os serviços

### 4. Acesse a Aplicação

Após o setup, acesse:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Dashboards:** http://localhost:8501
- **Documentação API:** http://localhost:8000/docs

## 🎯 Primeiros Passos

### 1. Criar Conta de Usuário

1. Acesse http://localhost:3000
2. Clique em "Criar Conta"
3. Preencha seus dados
4. Confirme o email

### 2. Configurar Primeiro Projeto

1. No dashboard, clique em "Novo Projeto"
2. Preencha as informações básicas
3. Selecione a metodologia (Scrum/Kanban)
4. Configure os membros da equipe

### 3. Usar o Chat IA

1. Vá para a seção "Chat IA"
2. Faça sua primeira pergunta sobre automação
3. Faça upload de documentos (PDF, imagens, áudio)
4. Veja a extração automática de requisitos

### 4. Explorar Dashboards

1. Acesse http://localhost:8501
2. Visualize os KPIs em tempo real
3. Explore os gráficos interativos
4. Configure filtros personalizados

## 🔧 Comandos Úteis

### Gerenciar Serviços

```bash
# Iniciar todos os serviços
docker-compose up -d

# Parar todos os serviços
docker-compose down

# Ver logs
docker-compose logs -f

# Reiniciar um serviço específico
docker-compose restart backend
```

### Desenvolvimento

```bash
# Backend em modo desenvolvimento
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend em modo desenvolvimento
cd frontend
npm install
npm start

# Dashboards em modo desenvolvimento
cd dashboards
pip install -r requirements.txt
streamlit run app.py
```

### Banco de Dados

```bash
# Acessar PostgreSQL
docker-compose exec postgres psql -U postgres -d milapp

# Backup do banco
docker-compose exec postgres pg_dump -U postgres milapp > backup.sql

# Restaurar backup
docker-compose exec -T postgres psql -U postgres milapp < backup.sql
```

## 🚨 Solução de Problemas

### Erro de Conexão com Banco

```bash
# Verificar se o PostgreSQL está rodando
docker-compose ps

# Reiniciar o banco
docker-compose restart postgres

# Verificar logs
docker-compose logs postgres
```

### Erro de OpenAI API

1. Verifique se a chave da API está correta no `.env`
2. Confirme se tem créditos disponíveis
3. Teste a conexão:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.openai.com/v1/models
```

### Frontend não Carrega

```bash
# Verificar se o React está rodando
docker-compose logs frontend

# Rebuild da imagem
docker-compose build frontend
docker-compose up -d frontend
```

### Dashboards não Acessíveis

```bash
# Verificar logs do Streamlit
docker-compose logs dashboards

# Reiniciar dashboards
docker-compose restart dashboards
```

## 📞 Suporte

Se encontrar problemas:

1. **Verifique os logs:** `docker-compose logs`
2. **Consulte a documentação:** [docs.milapp.com](https://docs.milapp.com)
3. **Abra uma issue:** [GitHub Issues](https://github.com/medsenior/milapp/issues)
4. **Entre em contato:** support@medsenior.com

## 🎉 Próximos Passos

Agora que o MILAPP está funcionando, explore:

- [Configuração Avançada](advanced-setup.md)
- [Guia de Uso Completo](user-guide.md)
- [API Reference](api-reference.md)
- [Deployment em Produção](deployment.md)

**Boa sorte com sua jornada de automação! 🚀**