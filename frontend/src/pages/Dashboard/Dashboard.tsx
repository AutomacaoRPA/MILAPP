import React from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
} from '@mui/material';
import { useDashboard } from '../../hooks/useDashboard';

const Dashboard: React.FC = () => {
  const { dashboardData, isLoading, error } = useDashboard();

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
          Erro ao carregar dados do dashboard. Tente novamente.
        </Alert>
      </Box>
    );
  }

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Dashboard Executivo
      </Typography>

      <Grid container spacing={3}>
        {/* KPIs */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total de Projetos
              </Typography>
              <Typography variant="h4">
                {dashboardData?.totalProjects || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Projetos Ativos
              </Typography>
              <Typography variant="h4">
                {dashboardData?.activeProjects || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Projetos Concluídos
              </Typography>
              <Typography variant="h4">
                {dashboardData?.completedProjects || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                ROI Médio
              </Typography>
              <Typography variant="h4">
                {dashboardData?.averageROI?.toFixed(1) || 0}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Projetos Recentes */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Projetos Recentes
              </Typography>
              {dashboardData?.recentProjects?.map((project) => (
                <Box key={project.id} mb={2} p={2} border="1px solid #eee" borderRadius={1}>
                  <Typography variant="subtitle1">{project.name}</Typography>
                  <Typography variant="body2" color="textSecondary">
                    Status: {project.status} | Progresso: {project.progress}%
                  </Typography>
                </Box>
              )) || (
                <Typography color="textSecondary">
                  Nenhum projeto recente encontrado.
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Alertas */}
        {dashboardData?.alerts && dashboardData.alerts.length > 0 && (
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Alertas e Notificações
                </Typography>
                {dashboardData.alerts.map((alert) => (
                  <Alert key={alert.id} severity={alert.type} sx={{ mb: 1 }}>
                    {alert.message}
                  </Alert>
                ))}
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default Dashboard; 