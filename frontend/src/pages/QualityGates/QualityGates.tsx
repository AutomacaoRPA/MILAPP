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
  LinearProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  PlayArrow as ExecuteIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  CheckCircle as PassedIcon,
  Cancel as FailedIcon,
} from '@mui/icons-material';
import { useQualityGates, useQualityGateTypes, useCreateQualityGate, useExecuteQualityGate, useDeleteQualityGate } from '../../hooks/useQualityGates';

const QualityGates: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [openCreateDialog, setOpenCreateDialog] = useState(false);
  const [selectedQualityGate, setSelectedQualityGate] = useState<any>(null);

  const { qualityGates, isLoading, error } = useQualityGates(0, 100);
  const { qualityGateTypes } = useQualityGateTypes();
  const createQualityGateMutation = useCreateQualityGate();
  const executeQualityGateMutation = useExecuteQualityGate();
  const deleteQualityGateMutation = useDeleteQualityGate();

  const filteredQualityGates = qualityGates.filter(qg => {
    const matchesSearch = qg.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         qg.project_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = !selectedStatus || qg.status === selectedStatus;
    return matchesSearch && matchesStatus;
  });

  const handleExecuteQualityGate = async (qualityGateId: string) => {
    try {
      await executeQualityGateMutation.mutateAsync(qualityGateId);
    } catch (error) {
      console.error('Erro ao executar quality gate:', error);
    }
  };

  const handleDeleteQualityGate = async (qualityGateId: string) => {
    if (window.confirm('Tem certeza que deseja deletar este quality gate?')) {
      try {
        await deleteQualityGateMutation.mutateAsync(qualityGateId);
      } catch (error) {
        console.error('Erro ao deletar quality gate:', error);
      }
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'passed':
        return 'success';
      case 'failed':
        return 'error';
      case 'pending':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'passed':
        return <PassedIcon />;
      case 'failed':
        return <FailedIcon />;
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
          Erro ao carregar quality gates. Tente novamente.
        </Alert>
      </Box>
    );
  }

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Quality Gates
      </Typography>

      {/* Filtros e Busca */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Buscar quality gates"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={selectedStatus}
                  onChange={(e) => setSelectedStatus(e.target.value)}
                  label="Status"
                >
                  <MenuItem value="">Todos</MenuItem>
                  <MenuItem value="passed">Aprovado</MenuItem>
                  <MenuItem value="failed">Reprovado</MenuItem>
                  <MenuItem value="pending">Pendente</MenuItem>
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
                Novo Quality Gate
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Lista de Quality Gates */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Nome</TableCell>
              <TableCell>Projeto</TableCell>
              <TableCell>Tipo</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Score</TableCell>
              <TableCell>Threshold</TableCell>
              <TableCell>Executado por</TableCell>
              <TableCell>Data</TableCell>
              <TableCell align="center">Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredQualityGates.map((qualityGate) => (
              <TableRow key={qualityGate.id}>
                <TableCell>
                  <Typography variant="subtitle2">{qualityGate.name}</Typography>
                </TableCell>
                <TableCell>{qualityGate.project_name}</TableCell>
                <TableCell>
                  <Chip 
                    label={qualityGateTypes.find(t => t.id === qualityGate.type)?.name || qualityGate.type}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    icon={getStatusIcon(qualityGate.status)}
                    label={qualityGate.status}
                    size="small"
                    color={getStatusColor(qualityGate.status) as any}
                  />
                </TableCell>
                <TableCell>
                  {qualityGate.score !== undefined ? (
                    <Box display="flex" alignItems="center">
                      <Typography variant="body2" sx={{ mr: 1 }}>
                        {qualityGate.score}%
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={qualityGate.score}
                        sx={{ width: 60, height: 6 }}
                        color={qualityGate.score >= (qualityGate.threshold || 0) ? 'success' : 'error'}
                      />
                    </Box>
                  ) : (
                    '-'
                  )}
                </TableCell>
                <TableCell>
                  {qualityGate.threshold ? `${qualityGate.threshold}%` : '-'}
                </TableCell>
                <TableCell>{qualityGate.executed_by || '-'}</TableCell>
                <TableCell>
                  {qualityGate.executed_at 
                    ? new Date(qualityGate.executed_at).toLocaleDateString('pt-BR')
                    : '-'
                  }
                </TableCell>
                <TableCell align="center">
                  <IconButton
                    size="small"
                    onClick={() => handleExecuteQualityGate(qualityGate.id)}
                    title="Executar"
                    color="primary"
                  >
                    <ExecuteIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => setSelectedQualityGate(qualityGate)}
                    title="Editar"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDeleteQualityGate(qualityGate.id)}
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
                Total de Quality Gates
              </Typography>
              <Typography variant="h4">
                {qualityGates.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Aprovados
              </Typography>
              <Typography variant="h4" color="success.main">
                {qualityGates.filter(qg => qg.status === 'passed').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Reprovados
              </Typography>
              <Typography variant="h4" color="error.main">
                {qualityGates.filter(qg => qg.status === 'failed').length}
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
                {qualityGates.length > 0 
                  ? `${((qualityGates.filter(qg => qg.status === 'passed').length / qualityGates.length) * 100).toFixed(1)}%`
                  : '0%'
                }
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Dialog de Criação */}
      <Dialog open={openCreateDialog} onClose={() => setOpenCreateDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Criar Novo Quality Gate</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
            Configure um novo quality gate para validação de qualidade.
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

export default QualityGates; 