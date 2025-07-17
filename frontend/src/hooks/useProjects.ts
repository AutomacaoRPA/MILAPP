import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';

export interface Project {
  id: string;
  name: string;
  description: string;
  status: string;
  priority: string;
  type: string;
  created_at: string;
  roi_target?: number;
  estimated_effort?: number;
}

export interface CreateProjectData {
  name: string;
  description: string;
  type: string;
  priority: string;
  roi_target?: number;
  estimated_effort?: number;
}

export interface UpdateProjectData extends Partial<CreateProjectData> {
  id: string;
}

export const useProjects = () => {
  const queryClient = useQueryClient();

  // Buscar todos os projetos
  const {
    data: projects,
    isLoading,
    error,
    refetch,
  } = useQuery<Project[]>({
    queryKey: ['projects'],
    queryFn: async () => {
      const response = await api.get('/projects/');
      return response.data;
    },
  });

  // Buscar projeto específico
  const useProject = (id: string) => {
    return useQuery<Project>({
      queryKey: ['projects', id],
      queryFn: async () => {
        const response = await api.get(`/projects/${id}/`);
        return response.data;
      },
      enabled: !!id,
    });
  };

  // Criar projeto
  const createProject = useMutation({
    mutationFn: async (data: CreateProjectData) => {
      const response = await api.post('/projects/', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
    },
  });

  // Atualizar projeto
  const updateProject = useMutation({
    mutationFn: async (data: UpdateProjectData) => {
      const { id, ...updateData } = data;
      const response = await api.put(`/projects/${id}/`, updateData);
      return response.data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
      queryClient.invalidateQueries({ queryKey: ['projects', data.id] });
    },
  });

  // Excluir projeto
  const deleteProject = useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/projects/${id}/`);
      return id;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
    },
  });

  return {
    projects,
    isLoading,
    error,
    refetch,
    useProject,
    createProject,
    updateProject,
    deleteProject,
  };
}; 