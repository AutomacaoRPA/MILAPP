# 📚 API Reference - MILAPP

Esta documentação descreve todos os endpoints da API do MILAPP.

## 🔗 Base URL

```
http://localhost:8000
```

## 🔐 Autenticação

A API usa JWT tokens para autenticação. Inclua o token no header:

```
Authorization: Bearer <your_jwt_token>
```

## 📋 Endpoints

### 🔐 Autenticação

#### POST /auth/register
Registra um novo usuário.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "João Silva",
  "role": "user"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "João Silva",
  "role": "user",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### POST /auth/login
Faz login do usuário.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "João Silva",
    "role": "user"
  }
}
```

### 💬 Conversas

#### GET /conversations
Lista todas as conversas do usuário.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "conversations": [
    {
      "id": 1,
      "title": "Automação de Processo RH",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T11:45:00Z",
      "message_count": 15
    }
  ]
}
```

#### POST /conversations
Cria uma nova conversa.

**Request Body:**
```json
{
  "title": "Nova Conversa",
  "initial_message": "Olá, preciso de ajuda com automação"
}
```

#### GET /conversations/{conversation_id}/messages
Lista mensagens de uma conversa.

**Parameters:**
- `conversation_id` (int): ID da conversa

**Response:**
```json
{
  "messages": [
    {
      "id": 1,
      "content": "Olá, como posso ajudar?",
      "role": "assistant",
      "created_at": "2024-01-15T10:30:00Z",
      "attachments": []
    }
  ]
}
```

#### POST /conversations/{conversation_id}/messages
Envia uma nova mensagem.

**Request Body:**
```json
{
  "content": "Preciso automatizar o processo de onboarding",
  "attachments": [
    {
      "type": "file",
      "url": "https://example.com/file.pdf"
    }
  ]
}
```

### 📋 Requisitos

#### GET /requirements
Lista requisitos extraídos.

**Query Parameters:**
- `project_id` (int, optional): Filtrar por projeto
- `status` (string, optional): Filtrar por status

**Response:**
```json
{
  "requirements": [
    {
      "id": 1,
      "title": "Automação de Onboarding",
      "description": "Automatizar processo de onboarding de funcionários",
      "priority": "high",
      "status": "draft",
      "extracted_from": "conversation_1",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### POST /requirements/extract
Extrai requisitos de uma conversa.

**Request Body:**
```json
{
  "conversation_id": 1,
  "extraction_type": "user_stories"
}
```

**Response:**
```json
{
  "requirements": [
    {
      "id": 1,
      "title": "Como usuário RH",
      "description": "quero automatizar o processo de onboarding",
      "acceptance_criteria": [
        "Sistema deve integrar com banco de dados de funcionários",
        "Processo deve ser aprovado por gestor"
      ],
      "priority": "high",
      "story_points": 8
    }
  ]
}
```

### 🛠️ Ferramentas RPA

#### GET /rpa/tools
Lista ferramentas RPA disponíveis.

**Response:**
```json
{
  "tools": [
    {
      "id": 1,
      "name": "n8n",
      "description": "Plataforma de automação open source",
      "category": "workflow_automation",
      "pros": ["Open source", "Fácil de usar"],
      "cons": ["Limitações em escala"],
      "best_for": ["Automações simples", "Prototipagem rápida"]
    }
  ]
}
```

#### POST /rpa/recommend
Recomenda ferramenta RPA baseada em requisitos.

**Request Body:**
```json
{
  "requirements": [
    {
      "title": "Automação de Processo RH",
      "description": "Automatizar onboarding de funcionários",
      "complexity": "medium",
      "budget": "low",
      "timeline": "3_months"
    }
  ]
}
```

**Response:**
```json
{
  "recommendation": {
    "tool": "n8n",
    "confidence": 0.85,
    "reasoning": "n8n é ideal para automações de processo de negócio...",
    "alternatives": [
      {
        "tool": "Python + Playwright",
        "confidence": 0.75,
        "reasoning": "Para maior controle e customização..."
      }
    ]
  }
}
```

### 📊 Projetos

#### GET /projects
Lista projetos do usuário.

**Response:**
```json
{
  "projects": [
    {
      "id": 1,
      "name": "Automação RH",
      "description": "Automatização completa do processo de RH",
      "status": "active",
      "methodology": "scrum",
      "created_at": "2024-01-15T10:30:00Z",
      "team_size": 5,
      "progress": 0.65
    }
  ]
}
```

#### POST /projects
Cria um novo projeto.

**Request Body:**
```json
{
  "name": "Novo Projeto",
  "description": "Descrição do projeto",
  "methodology": "scrum",
  "team_members": [1, 2, 3]
}
```

### 📈 Dashboards

#### GET /dashboard/kpis
Retorna KPIs do dashboard.

**Response:**
```json
{
  "kpis": {
    "total_projects": 15,
    "active_projects": 8,
    "completed_projects": 7,
    "total_automations": 45,
    "success_rate": 0.92,
    "time_saved_hours": 1200
  }
}
```

#### GET /dashboard/charts
Retorna dados para gráficos.

**Query Parameters:**
- `chart_type` (string): Tipo do gráfico
- `period` (string): Período (week, month, year)

**Response:**
```json
{
  "chart_data": {
    "labels": ["Jan", "Feb", "Mar"],
    "datasets": [
      {
        "label": "Projetos Concluídos",
        "data": [5, 8, 12]
      }
    ]
  }
}
```

## 🔄 Status Codes

- `200` - Sucesso
- `201` - Criado
- `400` - Bad Request
- `401` - Não autorizado
- `403` - Proibido
- `404` - Não encontrado
- `422` - Erro de validação
- `500` - Erro interno

## 📝 Exemplos de Uso

### Python

```python
import requests

# Login
response = requests.post('http://localhost:8000/auth/login', json={
    'email': 'user@example.com',
    'password': 'password'
})
token = response.json()['access_token']

# Criar conversa
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('http://localhost:8000/conversations', 
    json={'title': 'Nova Conversa'}, headers=headers)
conversation_id = response.json()['id']

# Enviar mensagem
response = requests.post(f'http://localhost:8000/conversations/{conversation_id}/messages',
    json={'content': 'Preciso automatizar um processo'}, headers=headers)
```

### JavaScript

```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        email: 'user@example.com',
        password: 'password'
    })
});
const {access_token} = await loginResponse.json();

// Listar projetos
const projectsResponse = await fetch('http://localhost:8000/projects', {
    headers: {'Authorization': `Bearer ${access_token}`}
});
const projects = await projectsResponse.json();
```

### cURL

```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Listar conversas
curl -X GET http://localhost:8000/conversations \
  -H "Authorization: Bearer <token>"
```

## 🔧 Testes

Teste a API usando o Swagger UI em:
```
http://localhost:8000/docs
```

## 📞 Suporte

Para dúvidas sobre a API:
- **Documentação:** [docs.milapp.com/api](https://docs.milapp.com/api)
- **Issues:** [GitHub Issues](https://github.com/medsenior/milapp/issues)
- **Email:** api-support@medsenior.com