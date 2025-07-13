import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  LinearProgress,
  Alert,
  Divider
} from '@mui/material';
import {
  Send as SendIcon,
  AttachFile as AttachFileIcon,
  Image as ImageIcon,
  Description as DescriptionIcon,
  Mic as MicIcon,
  Code as CodeIcon,
  Download as DownloadIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

interface Message {
  id: string;
  type: 'text' | 'image' | 'pdf' | 'audio' | 'bpmn' | 'system';
  role: 'user' | 'assistant' | 'system';
  content?: string;
  file_path?: string;
  file_name?: string;
  file_size?: number;
  ai_analysis?: any;
  created_at: string;
  is_processed: boolean;
  error_message?: string;
}

interface ChatInterfaceProps {
  conversationId?: string;
  projectId?: string;
  onRequirementsExtracted?: (requirements: any[]) => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  conversationId,
  projectId,
  onRequirementsExtracted
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [showFileDialog, setShowFileDialog] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Dropzone para upload de arquivos
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
      'application/pdf': ['.pdf'],
      'audio/*': ['.mp3', '.wav', '.m4a'],
      'text/xml': ['.bpmn', '.xml'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc']
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    onDrop: handleFileDrop
  });

  // Auto-scroll para a última mensagem
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Carrega mensagens existentes
  useEffect(() => {
    if (conversationId) {
      loadMessages();
    }
  }, [conversationId]);

  function scrollToBottom() {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }

  async function loadMessages() {
    try {
      const response = await axios.get(`/api/v1/conversations/${conversationId}/messages`);
      setMessages(response.data);
    } catch (error) {
      setError('Erro ao carregar mensagens');
      console.error('Erro ao carregar mensagens:', error);
    }
  }

  async function handleFileDrop(acceptedFiles: File[]) {
    for (const file of acceptedFiles) {
      await uploadFile(file);
    }
  }

  async function uploadFile(file: File) {
    setIsLoading(true);
    setUploadProgress(0);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('message_type', getFileType(file));
      formData.append('content', `Arquivo enviado: ${file.name}`);

      const response = await axios.post(
        `/api/v1/conversations/${conversationId}/messages`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (progressEvent) => {
            const progress = progressEvent.total
              ? Math.round((progressEvent.loaded * 100) / progressEvent.total)
              : 0;
            setUploadProgress(progress);
          },
        }
      );

      // Adiciona mensagens do usuário e da IA
      const userMessage: Message = {
        id: Date.now().toString(),
        type: getFileType(file),
        role: 'user',
        content: `Arquivo enviado: ${file.name}`,
        file_name: file.name,
        file_size: file.size,
        created_at: new Date().toISOString(),
        is_processed: true
      };

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'text',
        role: 'assistant',
        content: response.data.content,
        ai_analysis: response.data.ai_analysis,
        created_at: new Date().toISOString(),
        is_processed: response.data.is_processed,
        error_message: response.data.error_message
      };

      setMessages(prev => [...prev, userMessage, aiMessage]);
      setUploadProgress(0);

    } catch (error) {
      setError('Erro ao processar arquivo');
      console.error('Erro ao processar arquivo:', error);
    } finally {
      setIsLoading(false);
    }
  }

  function getFileType(file: File): string {
    if (file.type.startsWith('image/')) return 'image';
    if (file.type === 'application/pdf') return 'pdf';
    if (file.type.startsWith('audio/')) return 'audio';
    if (file.name.endsWith('.bpmn') || file.name.endsWith('.xml')) return 'bpmn';
    if (file.type.includes('spreadsheet') || file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) return 'excel';
    if (file.type.includes('word') || file.name.endsWith('.docx') || file.name.endsWith('.doc')) return 'word';
    return 'text';
  }

  async function sendMessage() {
    if (!inputValue.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('message_type', 'text');
      formData.append('content', inputValue);

      const response = await axios.post(
        `/api/v1/conversations/${conversationId}/messages`,
        formData
      );

      // Adiciona mensagens
      const userMessage: Message = {
        id: Date.now().toString(),
        type: 'text',
        role: 'user',
        content: inputValue,
        created_at: new Date().toISOString(),
        is_processed: true
      };

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'text',
        role: 'assistant',
        content: response.data.content,
        ai_analysis: response.data.ai_analysis,
        created_at: new Date().toISOString(),
        is_processed: response.data.is_processed,
        error_message: response.data.error_message
      };

      setMessages(prev => [...prev, userMessage, aiMessage]);
      setInputValue('');

    } catch (error) {
      setError('Erro ao enviar mensagem');
      console.error('Erro ao enviar mensagem:', error);
    } finally {
      setIsLoading(false);
    }
  }

  async function extractRequirements() {
    try {
      const response = await axios.post(`/api/v1/conversations/${conversationId}/extract-requirements`);
      
      if (onRequirementsExtracted) {
        onRequirementsExtracted(response.data.requirements);
      }

      // Adiciona mensagem do sistema
      const systemMessage: Message = {
        id: Date.now().toString(),
        type: 'system',
        role: 'system',
        content: `Requisitos extraídos: ${response.data.requirements.length} itens encontrados`,
        created_at: new Date().toISOString(),
        is_processed: true
      };

      setMessages(prev => [...prev, systemMessage]);

    } catch (error) {
      setError('Erro ao extrair requisitos');
      console.error('Erro ao extrair requisitos:', error);
    }
  }

  function getFileIcon(type: string) {
    switch (type) {
      case 'image': return <ImageIcon />;
      case 'pdf': return <DescriptionIcon />;
      case 'audio': return <MicIcon />;
      case 'bpmn': return <CodeIcon />;
      case 'excel': return <DescriptionIcon />;
      case 'word': return <DescriptionIcon />;
      default: return <DescriptionIcon />;
    }
  }

  function formatFileSize(bytes: number) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Paper elevation={1} sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6" component="h2">
            Chat IA - Levantamento de Requisitos
          </Typography>
          <Box>
            <Button
              variant="outlined"
              size="small"
              onClick={extractRequirements}
              disabled={messages.length === 0}
              sx={{ mr: 1 }}
            >
              Extrair Requisitos
            </Button>
            <Button
              variant="outlined"
              size="small"
              onClick={() => setShowFileDialog(true)}
            >
              Enviar Arquivo
            </Button>
          </Box>
        </Box>
      </Paper>

      {/* Messages */}
      <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
        <List>
          {messages.map((message) => (
            <ListItem
              key={message.id}
              sx={{
                flexDirection: 'column',
                alignItems: message.role === 'user' ? 'flex-end' : 'flex-start',
                mb: 2
              }}
            >
              <Box
                sx={{
                  maxWidth: '70%',
                  backgroundColor: message.role === 'user' ? 'primary.main' : 'grey.100',
                  color: message.role === 'user' ? 'white' : 'text.primary',
                  borderRadius: 2,
                  p: 2,
                  position: 'relative'
                }}
              >
                {/* Message Header */}
                <Box display="flex" alignItems="center" mb={1}>
                  <Avatar
                    sx={{
                      width: 24,
                      height: 24,
                      mr: 1,
                      bgcolor: message.role === 'user' ? 'primary.dark' : 'grey.500'
                    }}
                  >
                    {message.role === 'user' ? 'U' : 'IA'}
                  </Avatar>
                  <Typography variant="caption" sx={{ opacity: 0.7 }}>
                    {message.role === 'user' ? 'Você' : 'IA'} • {new Date(message.created_at).toLocaleTimeString()}
                  </Typography>
                  {message.type !== 'text' && (
                    <Chip
                      icon={getFileIcon(message.type)}
                      label={message.type.toUpperCase()}
                      size="small"
                      sx={{ ml: 1 }}
                    />
                  )}
                </Box>

                {/* Message Content */}
                {message.content && (
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    {message.content}
                  </Typography>
                )}

                {/* File Info */}
                {message.file_name && (
                  <Box display="flex" alignItems="center" sx={{ mb: 1 }}>
                    {getFileIcon(message.type)}
                    <Typography variant="caption" sx={{ ml: 1 }}>
                      {message.file_name} ({formatFileSize(message.file_size || 0)})
                    </Typography>
                  </Box>
                )}

                {/* AI Analysis */}
                {message.ai_analysis && !message.ai_analysis.error && (
                  <Box sx={{ mt: 1, p: 1, bgcolor: 'background.paper', borderRadius: 1 }}>
                    <Typography variant="caption" sx={{ fontWeight: 'bold' }}>
                      Análise IA:
                    </Typography>
                    <Typography variant="caption" display="block">
                      {JSON.stringify(message.ai_analysis, null, 2)}
                    </Typography>
                  </Box>
                )}

                {/* Error Message */}
                {message.error_message && (
                  <Alert severity="error" sx={{ mt: 1 }}>
                    {message.error_message}
                  </Alert>
                )}

                {/* Processing Status */}
                {!message.is_processed && (
                  <LinearProgress sx={{ mt: 1 }} />
                )}
              </Box>
            </ListItem>
          ))}
        </List>
        <div ref={messagesEndRef} />
      </Box>

      {/* Input Area */}
      <Paper elevation={1} sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {isLoading && (
          <Box sx={{ mb: 2 }}>
            <LinearProgress />
            <Typography variant="caption" sx={{ mt: 1 }}>
              Processando...
            </Typography>
          </Box>
        )}

        <Box display="flex" alignItems="center">
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Digite sua mensagem ou descreva o processo..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            disabled={isLoading}
            sx={{ mr: 1 }}
          />
          <IconButton
            color="primary"
            onClick={sendMessage}
            disabled={!inputValue.trim() || isLoading}
          >
            <SendIcon />
          </IconButton>
          <IconButton
            onClick={() => setShowFileDialog(true)}
            disabled={isLoading}
          >
            <AttachFileIcon />
          </IconButton>
        </Box>
      </Paper>

      {/* File Upload Dialog */}
      <Dialog open={showFileDialog} onClose={() => setShowFileDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Enviar Arquivo</DialogTitle>
        <DialogContent>
          <Box
            {...getRootProps()}
            sx={{
              border: '2px dashed',
              borderColor: isDragActive ? 'primary.main' : 'grey.300',
              borderRadius: 2,
              p: 3,
              textAlign: 'center',
              cursor: 'pointer',
              '&:hover': {
                borderColor: 'primary.main',
                backgroundColor: 'action.hover'
              }
            }}
          >
            <input {...getInputProps()} />
            <AttachFileIcon sx={{ fontSize: 48, color: 'grey.400', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              {isDragActive ? 'Solte os arquivos aqui' : 'Arraste arquivos ou clique para selecionar'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Suporta: imagens, PDFs, áudios, BPMN, Excel, Word
            </Typography>
            <Typography variant="caption" display="block" sx={{ mt: 1 }}>
              Máximo: 10MB por arquivo
            </Typography>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowFileDialog(false)}>Cancelar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ChatInterface;