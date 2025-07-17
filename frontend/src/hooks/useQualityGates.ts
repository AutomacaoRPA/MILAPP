import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';

export interface QualityGate {
  id: string;
  name: string;
  project_id: string;
  project_name: string;
  type: string;
  status: string;
  created_at: string;
  executed_at?: string;
  executed_by?: string;
  score?: number;
  threshold?: number;
  description?: string;
  criteria?: Array<{
    name: string;
    status: string;
    score: number;
  }>;
  logs?: Array<{
    timestamp: string;
    level: string;
    message: string;
  }>;
}

export interface QualityGateType {
  id: string;
  name: string;
}

export interface QualityGatesResponse {
  quality_gates: QualityGate[];
  total: number;
  skip: number;
  limit: number;
}

export const useQualityGates = (skip = 0, limit = 100, projectId?: string, status?: string) => {
  const {
    data: qualityGatesData,
    isLoading,
    error,
    refetch,
  } = useQuery<QualityGatesResponse>({
    queryKey: ['quality-gates', skip, limit, projectId, status],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (projectId) params.append('project_id', projectId);
      if (status) params.append('status', status);
      params.append('skip', skip.toString());
      params.append('limit', limit.toString());
      
      const response = await api.get(`/quality-gates?${params.toString()}`);
      return response.data;
    },
  });

  return {
    qualityGates: qualityGatesData?.quality_gates || [],
    total: qualityGatesData?.total || 0,
    isLoading,
    error,
    refetch,
  };
};

export const useQualityGate = (qualityGateId: string) => {
  const {
    data: qualityGate,
    isLoading,
    error,
    refetch,
  } = useQuery<QualityGate>({
    queryKey: ['quality-gate', qualityGateId],
    queryFn: async () => {
      const response = await api.get(`/quality-gates/${qualityGateId}`);
      return response.data;
    },
    enabled: !!qualityGateId,
  });

  return {
    qualityGate,
    isLoading,
    error,
    refetch,
  };
};

export const useQualityGateTypes = () => {
  const {
    data: qualityGateTypes,
    isLoading,
    error,
  } = useQuery<{ types: QualityGateType[] }>({
    queryKey: ['quality-gate-types'],
    queryFn: async () => {
      const response = await api.get('/quality-gates/types');
      return response.data;
    },
  });

  return {
    qualityGateTypes: qualityGateTypes?.types || [],
    isLoading,
    error,
  };
};

export const useCreateQualityGate = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: {
      name: string;
      project_id: string;
      quality_gate_type: string;
      threshold: number;
      description?: string;
    }) => {
      const response = await api.post('/quality-gates', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quality-gates'] });
    },
  });
};

export const useExecuteQualityGate = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (qualityGateId: string) => {
      const response = await api.post(`/quality-gates/${qualityGateId}/execute`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quality-gates'] });
    },
  });
};

export const useUpdateQualityGate = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ qualityGateId, data }: { qualityGateId: string; data: any }) => {
      const response = await api.put(`/quality-gates/${qualityGateId}`, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quality-gates'] });
    },
  });
};

export const useDeleteQualityGate = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (qualityGateId: string) => {
      const response = await api.delete(`/quality-gates/${qualityGateId}`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quality-gates'] });
    },
  });
};

export const useQualityGateMetrics = (qualityGateId: string) => {
  const {
    data: metrics,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['quality-gate-metrics', qualityGateId],
    queryFn: async () => {
      const response = await api.get(`/quality-gates/${qualityGateId}/metrics`);
      return response.data;
    },
    enabled: !!qualityGateId,
  });

  return {
    metrics: metrics?.metrics,
    isLoading,
    error,
  };
}; 