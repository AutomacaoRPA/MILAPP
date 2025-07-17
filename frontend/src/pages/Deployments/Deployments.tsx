import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Chip,
  Alert,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import {
  Add as AddIcon,
  PlayArrow as ExecuteIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  CheckCircle as SuccessIcon,
  Cancel as FailedIcon,
  Schedule as PendingIcon,
  Refresh as RollbackIcon,
} from '@mui/icons-material';
import { useDeployments, useEnvironments, useCreateDeployment, useExecuteDeployment, useRollbackDeployment, useDeleteDeployment } from '../../hooks/useDeployments';

const Deployments: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [selectedEnvironment, setSelectedEnvironment] = useState('');
  const [openCreateDialog, setOpenCreateDialog] = useState(false);
  const [selectedDeployment, setSelectedDeployment] = useState<any>(null);

  const { deployments, isLoading, error } = useDeployments(0, 100);
  const { environments } = useEnvironments();
  const createDeploymentMutation = useCreateDeployment();
  const executeDeploymentMutation = useExecuteDeployment();
  const rollbackDeploymentMutation = useRollbackDeployment();
  const deleteDeploymentMutation = useDeleteDeployment();

  const filteredDeployments = deployments.filter(dep => {
    const matchesSearch = dep.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         dep.project_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = !selectedStatus || dep.status === selectedStatus;
    const matchesEnvironment = !selectedEnvironment || dep.environment === selectedEnvironment;
    return matchesSearch && matchesStatus && matchesEnvironment;
  });

  const handleExecuteDeployment = async (deploymentId: string) => {
    try {
      await executeDeploymentMutation.mutateAsync(deploymentId);
    } catch (error) {
      console.error('Erro ao executar deployment:', error);
    }
  };

  const handleRollbackDeployment = async (deploymentId: string) => {
    if (window.confirm('Tem certeza que deseja fazer rollback deste deployment?')) {
      try {
        await rollbackDeploymentMutation.mutateAsync(deploymentId);
      } catch (error) {
        console.error('Erro ao fazer rollback:', error);
      }
    }
  };

  const handleDeleteDeployment = async (deploymentId: string) => {
    if (window.confirm('Tem certeza que deseja deletar este deployment?')) {
      try {
        await deleteDeploymentMutation.mutateAsync(deploymentId);
      } catch (error) {
        console.error('Erro ao deletar deployment:', error);
      }
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'failed':
        return 'error';
      case 'in_progress':
        return 'warning';
      case 'pending':
        return 'info';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <SuccessIcon />;
      case 'failed':
        return <FailedIcon />;
      case 'in_progress':
        return <PendingIcon />;
      default:
        return null;
    }
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={3}>
        <Alert severity="error">
          Erro ao carregar deployments. Tente novamente.
        </Alert>
      </Box>
    );
  }

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Deployments
      </Typography>

      {/* Filtros e Busca */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Buscar deployments"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={selectedStatus}
                  onChange={(e) => setSelectedStatus(e.target.value)}
                  label="Status"
                >
                  <MenuItem value="">Todos</MenuItem>
                  <MenuItem value="completed">Concluído</MenuItem>
                  <MenuItem value="failed">Falhou</MenuItem>
                  <MenuItem value="in_progress">Em Progresso</MenuItem>
                  <MenuItem value="pending">Pendente</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>Ambiente</InputLabel>
                <Select
                  value={selectedEnvironment}
                  onChange={(e) => setSelectedEnvironment(e.target.value)}
                  label="Ambiente"
                >
                  <MenuItem value="">Todos</MenuItem>
                  {environments.map((env) => (
                    <MenuItem key={env.id} value={env.id}>
                      {env.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <Button
                variant="outlined"
                startIcon={<FilterIcon />}
                fullWidth
              >
                Filtros
              </Button>
            </Grid>
            <Grid item xs={12} md={3}>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={() => setOpenCreateDialog(true)}
                fullWidth
              >
                Novo Deployment
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Lista de Deployments */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Nome</TableCell>
              <TableCell>Projeto</TableCell>
              <TableCell>Versão</TableCell>
              <TableCell>Ambiente</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Duração</TableCell>
              <TableCell>Deployado por</TableCell>
              <TableCell>Data</TableCell>
              <TableCell align="center">Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredDeployments.map((deployment) => (
              <TableRow key={deployment.id}>
                <TableCell>
                  <Typography variant="subtitle2">{deployment.name}</Typography>
                </TableCell>
                <TableCell>{deployment.project_name}</TableCell>
                <TableCell>
                  <Chip 
                    label={deployment.version}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                </TableCell>
                <TableCell>
                  <Chip 
                    label={environments.find(e => e.id === deployment.environment)?.name || deployment.environment}
                    size="small"
                    color="secondary"
                    variant="outlined"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    icon={getStatusIcon(deployment.status)}
                    label={deployment.status}
                    size="small"
                    color={getStatusColor(deployment.status) as any}
                  />
                </TableCell>
                <TableCell>{deployment.duration || '-'}</TableCell>
                <TableCell>{deployment.deployed_by || '-'}</TableCell>
                <TableCell>
                  {deployment.deployed_at 
                    ? new Date(deployment.deployed_at).toLocaleDateString('pt-BR')
                    : new Date(deployment.created_at).toLocaleDateString('pt-BR')
                  }
                </TableCell>
                <TableCell align="center">
                  <IconButton
                    size="small"
                    onClick={() => handleExecuteDeployment(deployment.id)}
                    title="Executar"
                    color="primary"
                    disabled={deployment.status === 'in_progress'}
                  >
                    <ExecuteIcon />
                  </IconButton>
                  {deployment.rollback_available && (
                    <IconButton
                      size="small"
                      onClick={() => handleRollbackDeployment(deployment.id)}
                      title="Rollback"
                      color="warning"
                    >
                      <RollbackIcon />
                    </IconButton>
                  )}
                  <IconButton
                    size="small"
                    onClick={() => setSelectedDeployment(deployment)}
                    title="Editar"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDeleteDeployment(deployment.id)}
                    title="Deletar"
                    color="error"
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Estatísticas */}
      <Grid container spacing={3} sx={{ mt: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total de Deployments
              </Typography>
              <Typography variant="h4">
                {deployments.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Concluídos
              </Typography>
              <Typography variant="h4" color="success.main">
                {deployments.filter(d => d.status === 'completed').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Falharam
              </Typography>
              <Typography variant="h4" color="error.main">
                {deployments.filter(d => d.status === 'failed').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Taxa de Sucesso
              </Typography>
              <Typography variant="h4">
                {deployments.length > 0 
                  ? `${((deployments.filter(d => d.status === 'completed').length / deployments.length) * 100).toFixed(1)}%`
                  : '0%'
                }
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Dialog de Criação */}
      <Dialog open={openCreateDialog} onClose={() => setOpenCreateDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Criar Novo Deployment</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
            Configure um novo deployment para o ambiente selecionado.
          </Typography>
          {/* Formulário seria implementado aqui */}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenCreateDialog(false)}>Cancelar</Button>
          <Button variant="contained" onClick={() => setOpenCreateDialog(false)}>
            Criar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Deployments; 