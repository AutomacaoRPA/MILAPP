# 🚀 Guia de Integração Frontend-Backend - MILAPP

## 📋 Visão Geral

Este guia explica como o frontend React/TypeScript do MILAPP está integrado ao backend FastAPI, incluindo autenticação, gerenciamento de estado e comunicação com APIs.

## 🔐 Sistema de Autenticação

### Contexto de Autenticação
O `AuthContext` gerencia o estado de autenticação globalmente:

```typescript
// Uso do contexto de autenticação
const { user, login, logout, loading } = useAuth();
```

### Fluxo de Login
1. **Formulário de Login** (`/pages/Login/Login.tsx`)
2. **Chamada à API** via `AuthContext`
3. **Armazenamento do Token** no localStorage
4. **Redirecionamento** para dashboard

### Proteção de Rotas
Todas as rotas protegidas usam o componente `ProtectedRoute`:

```typescript
<ProtectedRoute>
  <Layout>
    <Dashboard />
  </Layout>
</ProtectedRoute>
```

## 📡 Comunicação com API

### Configuração do Axios
O serviço de API está configurado em `services/api.ts`:

```typescript
// Configuração base
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
});

// Interceptor para token de autenticação
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Endpoints Principais

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/auth/login` | POST | Autenticação de usuário |
| `/auth/logout` | POST | Logout do usuário |
| `/projects/` | GET | Listar projetos |
| `/projects/` | POST | Criar projeto |
| `/projects/{id}` | GET | Obter projeto específico |
| `/projects/{id}` | PUT | Atualizar projeto |
| `/projects/{id}` | DELETE | Excluir projeto |
| `/dashboards/executive` | GET | Dados do dashboard executivo |

## 🎣 Hooks Personalizados

### useProjects
Gerencia operações CRUD de projetos:

```typescript
const { 
  projects, 
  isLoading, 
  error, 
  createProject, 
  updateProject, 
  deleteProject 
} = useProjects();
```

### useDashboard
Gerencia dados do dashboard executivo:

```typescript
const { 
  dashboardData, 
  isLoading, 
  error, 
  refetch 
} = useDashboard();
```

## 🔄 Gerenciamento de Estado

### React Query
Usado para cache e sincronização de dados:

```typescript
// Configuração global
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
```

### Invalidação de Cache
```typescript
// Após criar projeto
queryClient.invalidateQueries({ queryKey: ['projects'] });

// Após atualizar projeto específico
queryClient.invalidateQueries({ queryKey: ['projects', projectId] });
```

## 🎨 Componentes Principais

### Layout
- **AppBar** com menu de usuário
- **Drawer** com navegação
- **Proteção de rotas** integrada

### Dashboard
- **KPIs** em tempo real
- **Projetos recentes**
- **Alertas e notificações**

### Projects
- **Listagem** de projetos
- **Criação** via modal
- **Filtros** e busca

## 🛠️ Configuração de Ambiente

### Variáveis de Ambiente
Criar arquivo `.env`:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

### Dependências
```json
{
  "@tanstack/react-query": "^5.0.0",
  "@mui/material": "^5.15.0",
  "@mui/icons-material": "^5.15.0",
  "axios": "^1.6.0",
  "react-router-dom": "^6.8.0"
}
```

## 🔧 Desenvolvimento

### Estrutura de Arquivos
```
frontend/
├── src/
│   ├── components/
│   │   ├── Layout/
│   │   ├── ProtectedRoute/
│   │   └── ...
│   ├── pages/
│   │   ├── Login/
│   │   ├── Dashboard/
│   │   ├── Projects/
│   │   └── ...
│   ├── hooks/
│   │   ├── useProjects.ts
│   │   ├── useDashboard.ts
│   │   └── ...
│   ├── services/
│   │   └── api.ts
│   ├── contexts/
│   │   └── AuthContext.tsx
│   └── App.tsx
```

### Comandos de Desenvolvimento
```bash
# Instalar dependências
npm install

# Executar em desenvolvimento
npm start

# Build para produção
npm run build

# Executar testes
npm test
```

## 🚀 Deploy

### Build de Produção
```bash
npm run build
```

### Configuração do Servidor
- Configurar nginx para servir arquivos estáticos
- Configurar proxy para API
- Configurar HTTPS

### Docker
```dockerfile
FROM nginx:alpine
COPY build/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
```

## 🔍 Debugging

### Logs de Desenvolvimento
```typescript
// Habilitar logs detalhados
console.log('API Response:', response.data);
console.log('Auth State:', user);
```

### DevTools
- **React DevTools** para componentes
- **Redux DevTools** para estado
- **Network tab** para requisições

## 📊 Monitoramento

### Métricas de Performance
- **Tempo de carregamento** das páginas
- **Taxa de erro** das APIs
- **Uso de memória** do React Query

### Alertas
- **Falhas de autenticação**
- **Timeouts de API**
- **Erros de rede**

## 🔒 Segurança

### Validação de Token
```typescript
// Verificar token expirado
const token = localStorage.getItem('token');
if (token && isTokenExpired(token)) {
  logout();
}
```

### Sanitização de Dados
```typescript
// Sanitizar entrada do usuário
const sanitizedInput = DOMPurify.sanitize(userInput);
```

## 🧪 Testes

### Testes de Integração
```typescript
// Testar login
test('should login successfully', async () => {
  const { getByLabelText, getByRole } = render(<Login />);
  // ... implementação
});
```

### Testes de API
```typescript
// Mock de API
jest.mock('../services/api', () => ({
  get: jest.fn(),
  post: jest.fn(),
}));
```

## 📈 Próximos Passos

### Funcionalidades Pendentes
1. **Chat IA** - Integração com OpenAI
2. **Quality Gates** - Workflow de aprovação
3. **Deployments** - Pipeline CI/CD
4. **Documents** - Geração automática

### Melhorias Planejadas
1. **Offline Support** - Service Worker
2. **Real-time** - WebSocket
3. **PWA** - Progressive Web App
4. **Mobile** - Responsividade completa

---

**Este guia fornece uma visão completa da integração frontend-backend do MILAPP, permitindo desenvolvimento eficiente e manutenção adequada do sistema.** 