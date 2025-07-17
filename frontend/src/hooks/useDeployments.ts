import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';

export interface Deployment {
  id: string;
  name: string;
  project_id: string;
  project_name: string;
  version: string;
  environment: string;
  status: string;
  created_at: string;
  deployed_at?: string;
  deployed_by?: string;
  duration?: string;
  rollback_available: boolean;
  description?: string;
  changes?: string[];
  logs?: Array<{
    timestamp: string;
    level: string;
    message: string;
  }>;
  metrics?: {
    deployment_time: string;
    downtime: string;
    success_rate: number;
  };
}

export interface Environment {
  id: string;
  name: string;
}

export interface DeploymentsResponse {
  deployments: Deployment[];
  total: number;
  skip: number;
  limit: number;
}

export const useDeployments = (skip = 0, limit = 100, projectId?: string, status?: string, environment?: string) => {
  const {
    data: deploymentsData,
    isLoading,
    error,
    refetch,
  } = useQuery<DeploymentsResponse>({
    queryKey: ['deployments', skip, limit, projectId, status, environment],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (projectId) params.append('project_id', projectId);
      if (status) params.append('status', status);
      if (environment) params.append('environment', environment);
      params.append('skip', skip.toString());
      params.append('limit', limit.toString());
      
      const response = await api.get(`/deployments?${params.toString()}`);
      return response.data;
    },
  });

  return {
    deployments: deploymentsData?.deployments || [],
    total: deploymentsData?.total || 0,
    isLoading,
    error,
    refetch,
  };
};

export const useDeployment = (deploymentId: string) => {
  const {
    data: deployment,
    isLoading,
    error,
    refetch,
  } = useQuery<Deployment>({
    queryKey: ['deployment', deploymentId],
    queryFn: async () => {
      const response = await api.get(`/deployments/${deploymentId}`);
      return response.data;
    },
    enabled: !!deploymentId,
  });

  return {
    deployment,
    isLoading,
    error,
    refetch,
  };
};

export const useEnvironments = () => {
  const {
    data: environments,
    isLoading,
    error,
  } = useQuery<{ environments: Environment[] }>({
    queryKey: ['environments'],
    queryFn: async () => {
      const response = await api.get('/deployments/environments');
      return response.data;
    },
  });

  return {
    environments: environments?.environments || [],
    isLoading,
    error,
  };
};

export const useCreateDeployment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: {
      project_id: string;
      version: string;
      environment: string;
      description?: string;
    }) => {
      const response = await api.post('/deployments', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deployments'] });
    },
  });
};

export const useExecuteDeployment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (deploymentId: string) => {
      const response = await api.post(`/deployments/${deploymentId}/execute`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deployments'] });
    },
  });
};

export const useRollbackDeployment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (deploymentId: string) => {
      const response = await api.post(`/deployments/${deploymentId}/rollback`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deployments'] });
    },
  });
};

export const useUpdateDeployment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ deploymentId, data }: { deploymentId: string; data: any }) => {
      const response = await api.put(`/deployments/${deploymentId}`, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deployments'] });
    },
  });
};

export const useDeleteDeployment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (deploymentId: string) => {
      const response = await api.delete(`/deployments/${deploymentId}`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deployments'] });
    },
  });
};

export const useDeploymentLogs = (deploymentId: string) => {
  const {
    data: logs,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['deployment-logs', deploymentId],
    queryFn: async () => {
      const response = await api.get(`/deployments/${deploymentId}/logs`);
      return response.data;
    },
    enabled: !!deploymentId,
  });

  return {
    logs: logs?.logs || [],
    isLoading,
    error,
  };
}; 