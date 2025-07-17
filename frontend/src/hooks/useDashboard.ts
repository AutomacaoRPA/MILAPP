import { useQuery } from '@tanstack/react-query';
import api from '../services/api';

export interface DashboardData {
  totalProjects: number;
  activeProjects: number;
  completedProjects: number;
  totalROI: number;
  averageROI: number;
  recentProjects: Array<{
    id: string;
    name: string;
    status: string;
    progress: number;
  }>;
  alerts: Array<{
    id: string;
    type: 'info' | 'warning' | 'error' | 'success';
    message: string;
    timestamp: string;
  }>;
  metrics: {
    productivity: number;
    quality: number;
    efficiency: number;
  };
}

export const useDashboard = () => {
  const {
    data: dashboardData,
    isLoading,
    error,
    refetch,
  } = useQuery<DashboardData>({
    queryKey: ['dashboard'],
    queryFn: async () => {
      const response = await api.get('/dashboards/executive');
      return response.data;
    },
    refetchInterval: 30000, // Atualizar a cada 30 segundos
  });

  return {
    dashboardData,
    isLoading,
    error,
    refetch,
  };
}; 