import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';

export interface Document {
  id: string;
  name: string;
  type: string;
  project_id: string;
  project_name: string;
  size: string;
  uploaded_at: string;
  uploaded_by: string;
  status: string;
  description?: string;
  tags?: string[];
  version?: string;
  download_url?: string;
}

export interface DocumentType {
  id: string;
  name: string;
}

export interface DocumentsResponse {
  documents: Document[];
  total: number;
  skip: number;
  limit: number;
}

export const useDocuments = (skip = 0, limit = 100, projectId?: string, documentType?: string) => {
  const {
    data: documentsData,
    isLoading,
    error,
    refetch,
  } = useQuery<DocumentsResponse>({
    queryKey: ['documents', skip, limit, projectId, documentType],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (projectId) params.append('project_id', projectId);
      if (documentType) params.append('document_type', documentType);
      params.append('skip', skip.toString());
      params.append('limit', limit.toString());
      
      const response = await api.get(`/documents?${params.toString()}`);
      return response.data;
    },
  });

  return {
    documents: documentsData?.documents || [],
    total: documentsData?.total || 0,
    isLoading,
    error,
    refetch,
  };
};

export const useDocument = (documentId: string) => {
  const {
    data: document,
    isLoading,
    error,
    refetch,
  } = useQuery<Document>({
    queryKey: ['document', documentId],
    queryFn: async () => {
      const response = await api.get(`/documents/${documentId}`);
      return response.data;
    },
    enabled: !!documentId,
  });

  return {
    document,
    isLoading,
    error,
    refetch,
  };
};

export const useDocumentTypes = () => {
  const {
    data: documentTypes,
    isLoading,
    error,
  } = useQuery<{ types: DocumentType[] }>({
    queryKey: ['document-types'],
    queryFn: async () => {
      const response = await api.get('/documents/types');
      return response.data;
    },
  });

  return {
    documentTypes: documentTypes?.types || [],
    isLoading,
    error,
  };
};

export const useCreateDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (formData: FormData) => {
      const response = await api.post('/documents', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });
};

export const useUpdateDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ documentId, data }: { documentId: string; data: FormData }) => {
      const response = await api.put(`/documents/${documentId}`, data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });
};

export const useDeleteDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (documentId: string) => {
      const response = await api.delete(`/documents/${documentId}`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });
}; 