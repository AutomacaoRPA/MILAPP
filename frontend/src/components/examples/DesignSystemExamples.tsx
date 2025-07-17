import React from 'react';
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  Chip,
  LinearProgress,
  CircularProgress,
  TextField,
  Typography,
  Box,
  Grid,
  Paper,
  Divider,
  Alert,
  AlertTitle,
} from '@mui/material';
import {
  Add as AddIcon,
  Check as CheckIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
} from '@mui/icons-material';

/**
 * Exemplos de componentes usando o Design System do MILAPP
 * Este arquivo demonstra como usar os componentes e cores do tema
 */
const DesignSystemExamples: React.FC = () => {
  return (
    <Box sx={{ p: 4, maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h3" gutterBottom>
        MILAPP Design System - Exemplos
      </Typography>
      
      {/* Seção de Cores */}
      <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>
        Paleta de Cores
      </Typography>
      
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Cores Primárias */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Cores Primárias" />
            <CardContent>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {[50, 100, 200, 300, 400, 500, 600, 700, 800, 900].map((shade) => (
                  <Box
                    key={shade}
                    sx={{
                      width: 60,
                      height: 60,
                      bgcolor: `primary.${shade}`,
                      borderRadius: 1,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: shade <= 400 ? 'text.primary' : 'white',
                      fontSize: '0.75rem',
                      fontWeight: 'bold',
                    }}
                  >
                    {shade}
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Cores de Status */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Cores de Status" />
            <CardContent>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Alert severity="success" icon={<CheckIcon />}>
                  Operação realizada com sucesso
                </Alert>
                <Alert severity="warning" icon={<WarningIcon />}>
                  Atenção: ação requer confirmação
                </Alert>
                <Alert severity="error" icon={<ErrorIcon />}>
                  Erro: operação falhou
                </Alert>
                <Alert severity="info" icon={<InfoIcon />}>
                  Informação importante
                </Alert>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      {/* Seção de Botões */}
      <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>
        Botões
      </Typography>
      
      <Card sx={{ mb: 4 }}>
        <CardHeader title="Variações de Botões" />
        <CardContent>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            <Button variant="contained" color="primary">
              Primário
            </Button>
            <Button variant="outlined" color="primary">
              Secundário
            </Button>
            <Button variant="text" color="primary">
              Texto
            </Button>
            <Button variant="contained" color="success">
              Sucesso
            </Button>
            <Button variant="contained" color="error">
              Erro
            </Button>
            <Button variant="contained" color="warning">
              Aviso
            </Button>
            <Button variant="contained" color="info">
              Info
            </Button>
            <Button variant="contained" disabled>
              Desabilitado
            </Button>
          </Box>
          
          <Divider sx={{ my: 3 }} />
          
          <Typography variant="h6" gutterBottom>
            Tamanhos
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Button variant="contained" size="small">
              Pequeno
            </Button>
            <Button variant="contained" size="medium">
              Médio
            </Button>
            <Button variant="contained" size="large">
              Grande
            </Button>
          </Box>
          
          <Divider sx={{ my: 3 }} />
          
          <Typography variant="h6" gutterBottom>
            Com Ícones
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button variant="contained" startIcon={<AddIcon />}>
              Adicionar
            </Button>
            <Button variant="outlined" endIcon={<CheckIcon />}>
              Confirmar
            </Button>
          </Box>
        </CardContent>
      </Card>
      
      {/* Seção de Chips */}
      <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>
        Chips
      </Typography>
      
      <Card sx={{ mb: 4 }}>
        <CardHeader title="Variações de Chips" />
        <CardContent>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            <Chip label="Tag" color="primary" />
            <Chip label="Aprovado" color="success" />
            <Chip label="Pendente" color="warning" />
            <Chip label="Erro" color="error" />
            <Chip label="Info" color="info" />
            <Chip label="Deletável" onDelete={() => {}} />
            <Chip label="Clicável" onClick={() => {}} />
            <Chip label="Desabilitado" disabled />
          </Box>
        </CardContent>
      </Card>
      
      {/* Seção de Progress */}
      <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>
        Indicadores de Progresso
      </Typography>
      
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Progresso Linear" />
            <CardContent>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box>
                  <Typography variant="body2" gutterBottom>
                    Progresso 25%
                  </Typography>
                  <LinearProgress variant="determinate" value={25} />
                </Box>
                <Box>
                  <Typography variant="body2" gutterBottom>
                    Progresso 50%
                  </Typography>
                  <LinearProgress variant="determinate" value={50} />
                </Box>
                <Box>
                  <Typography variant="body2" gutterBottom>
                    Progresso 75%
                  </Typography>
                  <LinearProgress variant="determinate" value={75} />
                </Box>
                <Box>
                  <Typography variant="body2" gutterBottom>
                    Progresso Indeterminado
                  </Typography>
                  <LinearProgress />
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Progresso Circular" />
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-around' }}>
                <Box sx={{ textAlign: 'center' }}>
                  <CircularProgress variant="determinate" value={25} />
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    25%
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <CircularProgress variant="determinate" value={50} />
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    50%
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <CircularProgress variant="determinate" value={75} />
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    75%
                  </Typography>
                </Box>
                <Box sx={{ textAlign: 'center' }}>
                  <CircularProgress />
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    Indeterminado
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      {/* Seção de Formulários */}
      <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>
        Campos de Formulário
      </Typography>
      
      <Card sx={{ mb: 4 }}>
        <CardHeader title="Campos de Texto" />
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Campo Normal"
                placeholder="Digite aqui..."
                helperText="Texto de ajuda"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Campo com Erro"
                error
                helperText="Campo obrigatório"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Campo Desabilitado"
                disabled
                value="Valor fixo"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Campo com Ícone"
                InputProps={{
                  startAdornment: <AddIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                }}
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>
      
      {/* Seção de Tipografia */}
      <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>
        Tipografia
      </Typography>
      
      <Card sx={{ mb: 4 }}>
        <CardHeader title="Hierarquia de Texto" />
        <CardContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography variant="h1">Título H1 - 2.5rem</Typography>
            <Typography variant="h2">Título H2 - 2rem</Typography>
            <Typography variant="h3">Título H3 - 1.75rem</Typography>
            <Typography variant="h4">Título H4 - 1.5rem</Typography>
            <Typography variant="h5">Título H5 - 1.25rem</Typography>
            <Typography variant="h6">Título H6 - 1.125rem</Typography>
            <Typography variant="subtitle1">Subtítulo 1 - 1rem</Typography>
            <Typography variant="subtitle2">Subtítulo 2 - 0.875rem</Typography>
            <Typography variant="body1">
              Corpo 1 - 1rem. Este é um exemplo de texto do corpo principal.
            </Typography>
            <Typography variant="body2">
              Corpo 2 - 0.875rem. Este é um exemplo de texto secundário.
            </Typography>
            <Typography variant="caption">
              Caption - 0.75rem. Texto pequeno para legendas.
            </Typography>
            <Typography variant="overline">
              Overline - 0.75rem. Texto em maiúsculas para títulos.
            </Typography>
          </Box>
        </CardContent>
      </Card>
      
      {/* Seção de Cards */}
      <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>
        Cards
      </Typography>
      
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader
              title="Card Simples"
              subheader="Subtítulo do card"
            />
            <CardContent>
              <Typography variant="body2">
                Este é um exemplo de card simples com conteúdo básico.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader
              title="Card com Ações"
              subheader="Card com botões de ação"
            />
            <CardContent>
              <Typography variant="body2">
                Este card demonstra como adicionar ações.
              </Typography>
            </CardContent>
            <Box sx={{ p: 2, display: 'flex', gap: 1 }}>
              <Button size="small" variant="outlined">
                Cancelar
              </Button>
              <Button size="small" variant="contained">
                Confirmar
              </Button>
            </Box>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader
              title="Card com Progresso"
              subheader="Card com indicador de progresso"
            />
            <CardContent>
              <Typography variant="body2" gutterBottom>
                Progresso do projeto
              </Typography>
              <LinearProgress variant="determinate" value={65} />
              <Typography variant="body2" sx={{ mt: 1 }}>
                65% completo
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      {/* Seção de Espaçamento */}
      <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>
        Sistema de Espaçamento
      </Typography>
      
      <Card sx={{ mb: 4 }}>
        <CardHeader title="Demonstração de Espaçamento" />
        <CardContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Paper sx={{ p: 1, bgcolor: 'primary.100' }}>
              <Typography variant="body2">Espaçamento 1 (4px)</Typography>
            </Paper>
            <Paper sx={{ p: 2, bgcolor: 'primary.200' }}>
              <Typography variant="body2">Espaçamento 2 (8px)</Typography>
            </Paper>
            <Paper sx={{ p: 3, bgcolor: 'primary.300' }}>
              <Typography variant="body2">Espaçamento 3 (12px)</Typography>
            </Paper>
            <Paper sx={{ p: 4, bgcolor: 'primary.400' }}>
              <Typography variant="body2">Espaçamento 4 (16px)</Typography>
            </Paper>
            <Paper sx={{ p: 6, bgcolor: 'primary.500' }}>
              <Typography variant="body2" sx={{ color: 'white' }}>
                Espaçamento 6 (24px)
              </Typography>
            </Paper>
          </Box>
        </CardContent>
      </Card>
      
      {/* Seção de Responsividade */}
      <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>
        Responsividade
      </Typography>
      
      <Card sx={{ mb: 4 }}>
        <CardHeader title="Grid Responsivo" />
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={4} lg={3}>
              <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'primary.100' }}>
                <Typography variant="body2">xs=12 sm=6 md=4 lg=3</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={4} lg={3}>
              <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'secondary.100' }}>
                <Typography variant="body2">xs=12 sm=6 md=4 lg=3</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={4} lg={3}>
              <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'warning.100' }}>
                <Typography variant="body2">xs=12 sm=6 md=4 lg=3</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={4} lg={3}>
              <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'error.100' }}>
                <Typography variant="body2">xs=12 sm=6 md=4 lg=3</Typography>
              </Paper>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
      
      {/* Seção de Acessibilidade */}
      <Typography variant="h4" sx={{ mt: 4, mb: 2 }}>
        Acessibilidade
      </Typography>
      
      <Card sx={{ mb: 4 }}>
        <CardHeader title="Recursos de Acessibilidade" />
        <CardContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Alert severity="info">
              <AlertTitle>Navegação por Teclado</AlertTitle>
              Todos os componentes suportam navegação por teclado. Use Tab para navegar e Enter/Space para ativar.
            </Alert>
            
            <Alert severity="info">
              <AlertTitle>Alto Contraste</AlertTitle>
              O design system suporta modo de alto contraste para melhor acessibilidade.
            </Alert>
            
            <Alert severity="info">
              <AlertTitle>Redução de Movimento</AlertTitle>
              As animações respeitam as preferências de movimento reduzido do usuário.
            </Alert>
            
            <Alert severity="info">
              <AlertTitle>Leitores de Tela</AlertTitle>
              Todos os componentes incluem suporte adequado para leitores de tela.
            </Alert>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default DesignSystemExamples; 