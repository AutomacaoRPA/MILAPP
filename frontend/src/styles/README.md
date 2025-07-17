# MILAPP Design System

## Visão Geral

O Design System do MILAPP foi criado para garantir consistência visual e experiência do usuário em toda a plataforma. Ele segue princípios modernos de design com foco em usabilidade, acessibilidade e eficiência.

## Paleta de Cores

### Cores Primárias - Azul Corporativo
- **Primary 50**: `#eff6ff` - Fundo muito claro
- **Primary 100**: `#dbeafe` - Fundo claro
- **Primary 200**: `#bfdbfe` - Borda clara
- **Primary 300**: `#93c5fd` - Hover states
- **Primary 400**: `#60a5fa` - Links e interações
- **Primary 500**: `#3b82f6` - Elementos ativos
- **Primary 600**: `#2563eb` - Cor principal
- **Primary 700**: `#1d4ed8` - Hover principal
- **Primary 800**: `#1e40af` - Estados pressionados
- **Primary 900**: `#1e3a8a` - Texto em fundo claro
- **Primary 950**: `#172554` - Texto em fundo muito claro

### Cores Secundárias - Verde Sucesso
- **Secondary 50**: `#f0fdf4` - Fundo sucesso
- **Secondary 100**: `#dcfce7` - Borda sucesso
- **Secondary 500**: `#22c55e` - Sucesso principal
- **Secondary 600**: `#16a34a` - Hover sucesso
- **Secondary 700**: `#15803d` - Estados pressionados

### Cores de Acento - Laranja Energia
- **Accent 50**: `#fff7ed` - Fundo acento
- **Accent 100**: `#ffedd5` - Borda acento
- **Accent 500**: `#f97316` - Acento principal
- **Accent 600**: `#ea580c` - Hover acento
- **Accent 700**: `#c2410c` - Estados pressionados

### Cores de Status
- **Success**: `#22c55e` - Operações bem-sucedidas
- **Warning**: `#f59e0b` - Avisos e alertas
- **Error**: `#ef4444` - Erros e falhas
- **Info**: `#3b82f6` - Informações

### Cores Neutras
- **Neutral 50**: `#fafafa` - Fundo mais claro
- **Neutral 100**: `#f5f5f5` - Fundo claro
- **Neutral 200**: `#e5e5e5` - Bordas
- **Neutral 300**: `#d4d4d4` - Divisores
- **Neutral 400**: `#a3a3a3` - Texto secundário
- **Neutral 500**: `#737373` - Texto terciário
- **Neutral 600**: `#525252` - Texto principal
- **Neutral 700**: `#404040` - Texto forte
- **Neutral 800**: `#262626` - Texto muito forte
- **Neutral 900**: `#171717` - Texto mais forte
- **Neutral 950**: `#0a0a0a` - Texto mais forte

## Tipografia

### Família de Fontes
- **Primária**: Inter - Para interface geral
- **Monospace**: JetBrains Mono - Para código

### Escalas Tipográficas
- **XS**: 12px - Labels pequenos
- **SM**: 14px - Texto secundário
- **Base**: 16px - Texto do corpo
- **LG**: 18px - Texto destacado
- **XL**: 20px - Subtítulos
- **2XL**: 24px - Títulos pequenos
- **3XL**: 30px - Títulos médios
- **4XL**: 36px - Títulos grandes
- **5XL**: 48px - Títulos muito grandes
- **6XL**: 60px - Títulos enormes

### Pesos de Fonte
- **Light**: 300 - Texto muito fino
- **Normal**: 400 - Texto normal
- **Medium**: 500 - Texto médio
- **Semibold**: 600 - Texto semi-negrito
- **Bold**: 700 - Texto negrito
- **Extrabold**: 800 - Texto muito negrito

## Componentes

### Botões
```tsx
// Botão primário
<Button variant="contained" color="primary">
  Ação Principal
</Button>

// Botão secundário
<Button variant="outlined" color="primary">
  Ação Secundária
</Button>

// Botão de sucesso
<Button variant="contained" color="success">
  Confirmar
</Button>

// Botão de erro
<Button variant="contained" color="error">
  Cancelar
</Button>
```

### Cards
```tsx
<Card>
  <CardHeader title="Título do Card" />
  <CardContent>
    Conteúdo do card
  </CardContent>
  <CardActions>
    <Button>Ação</Button>
  </CardActions>
</Card>
```

### Chips
```tsx
// Chip primário
<Chip label="Tag" color="primary" />

// Chip de sucesso
<Chip label="Aprovado" color="success" />

// Chip de aviso
<Chip label="Pendente" color="warning" />

// Chip de erro
<Chip label="Erro" color="error" />
```

### Progress Bars
```tsx
// Barra de progresso linear
<LinearProgress variant="determinate" value={75} />

// Progresso circular
<CircularProgress variant="determinate" value={75} />
```

## Espaçamento

### Sistema de Espaçamento
- **0**: 0px
- **1**: 4px
- **2**: 8px
- **3**: 12px
- **4**: 16px
- **5**: 20px
- **6**: 24px
- **8**: 32px
- **10**: 40px
- **12**: 48px
- **16**: 64px
- **20**: 80px
- **24**: 96px
- **32**: 128px
- **40**: 160px
- **48**: 192px
- **56**: 224px
- **64**: 256px

## Bordas e Raios

### Raios de Borda
- **None**: 0px
- **SM**: 2px
- **Base**: 4px
- **MD**: 6px
- **LG**: 8px
- **XL**: 12px
- **2XL**: 16px
- **3XL**: 24px
- **Full**: 9999px

## Sombras

### Sistema de Sombras
- **XS**: `0 1px 2px 0 rgba(0, 0, 0, 0.05)`
- **SM**: `0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)`
- **MD**: `0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)`
- **LG**: `0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)`
- **XL**: `0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)`
- **2XL**: `0 25px 50px -12px rgba(0, 0, 0, 0.25)`

## Animações

### Durações
- **75ms**: Animações muito rápidas
- **100ms**: Animações rápidas
- **150ms**: Animações médias-rápidas
- **200ms**: Animações médias
- **300ms**: Animações padrão
- **500ms**: Animações lentas
- **700ms**: Animações muito lentas
- **1000ms**: Animações extremamente lentas

### Funções de Easing
- **Linear**: `linear`
- **Ease In**: `cubic-bezier(0.4, 0, 1, 1)`
- **Ease Out**: `cubic-bezier(0, 0, 0.2, 1)`
- **Ease In Out**: `cubic-bezier(0.4, 0, 0.2, 1)`
- **Bounce**: `cubic-bezier(0.68, -0.55, 0.265, 1.55)`

## Breakpoints

### Sistema Responsivo
- **XS**: 0px - Mobile pequeno
- **SM**: 640px - Mobile grande
- **MD**: 768px - Tablet
- **LG**: 1024px - Desktop pequeno
- **XL**: 1280px - Desktop médio
- **2XL**: 1536px - Desktop grande

## Acessibilidade

### Navegação por Teclado
```css
.focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
  border-radius: var(--radius-base);
}
```

### Alto Contraste
```css
@media (prefers-contrast: high) {
  :root {
    --primary-500: #0066cc;
    --text-primary: #000000;
    --bg-primary: #ffffff;
    --border-color: #000000;
  }
}
```

### Redução de Movimento
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Uso no Projeto

### Importando o Tema
```tsx
import { ThemeProvider } from '@mui/material/styles';
import theme from './styles/theme';

function App() {
  return (
    <ThemeProvider theme={theme}>
      {/* Seu app aqui */}
    </ThemeProvider>
  );
}
```

### Usando Cores
```tsx
import { colors } from './styles/theme';

// Usando cores diretamente
const primaryColor = colors.primary[600];
const successColor = colors.success[500];
```

### Usando Classes CSS
```tsx
// Classes utilitárias
<div className="bg-primary-500 text-white p-4 rounded-lg">
  Conteúdo
</div>

// Componentes específicos
<div className="card">
  <div className="card-header">
    Título
  </div>
  <div className="card-body">
    Conteúdo
  </div>
</div>
```

## Princípios de Design

### 1. Consistência
- Use sempre os mesmos componentes para as mesmas funcionalidades
- Mantenha a hierarquia visual consistente
- Siga os padrões de espaçamento e tipografia

### 2. Simplicidade
- Priorize a clareza sobre a complexidade
- Use cores e elementos visuais com propósito
- Evite sobrecarregar a interface

### 3. Acessibilidade
- Garanta contraste adequado
- Suporte navegação por teclado
- Respeite preferências de movimento reduzido

### 4. Responsividade
- Design mobile-first
- Adapte componentes para diferentes tamanhos de tela
- Mantenha a usabilidade em todos os dispositivos

### 5. Performance
- Use animações com moderação
- Otimize para carregamento rápido
- Considere o impacto na performance

## Contribuindo

### Adicionando Novos Componentes
1. Defina o componente no design system
2. Documente seu uso e variações
3. Implemente no tema do Material-UI
4. Adicione exemplos de uso

### Modificando Cores
1. Atualize a paleta no arquivo `theme.ts`
2. Teste em diferentes contextos
3. Verifique acessibilidade
4. Atualize a documentação

### Adicionando Animações
1. Defina a duração e easing
2. Teste com preferências de movimento reduzido
3. Considere o impacto na performance
4. Documente o uso

## Recursos

- [Material-UI Documentation](https://mui.com/)
- [Inter Font](https://rsms.me/inter/)
- [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
- [Color Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/) 