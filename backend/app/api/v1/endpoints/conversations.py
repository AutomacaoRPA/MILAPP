"""
Endpoints para conversações IA do MILAPP
"""

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import structlog

from app.core.security import get_current_user
from app.services.ai_service import AIService
from app.models.user import User

logger = structlog.get_logger()

router = APIRouter()


# Schemas
class MessageCreate(BaseModel):
    """Schema para criação de mensagem"""
    content: str
    conversation_id: Optional[str] = None
    context: Optional[dict] = None


class MessageResponse(BaseModel):
    """Schema de resposta de mensagem"""
    id: str
    conversation_id: str
    type: str
    content: str
    ai_analysis: Optional[dict] = None
    created_at: str


class ConversationCreate(BaseModel):
    """Schema para criação de conversa"""
    title: str
    project_id: Optional[str] = None


class ConversationResponse(BaseModel):
    """Schema de resposta de conversa"""
    id: str
    title: str
    project_id: Optional[str] = None
    status: str
    ai_summary: Optional[str] = None
    extracted_requirements: List[dict]
    confidence_score: float
    created_at: str
    updated_at: str


# Endpoints
@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate,
    current_user: User = Depends(get_current_user)
):
    """Criar nova conversa com IA"""
    try:
        conversation_id = str(uuid.uuid4())
        
        # Criar conversa no banco
        conversation_data = {
            "id": conversation_id,
            "title": conversation.title,
            "project_id": conversation.project_id,
            "user_id": current_user.id,
            "status": "active"
        }
        
        # Por enquanto, retornar dados mock
        return ConversationResponse(
            id=conversation_id,
            title=conversation.title,
            project_id=conversation.project_id,
            status="active",
            ai_summary=None,
            extracted_requirements=[],
            confidence_score=0.0,
            created_at="2025-01-01T00:00:00Z",
            updated_at="2025-01-01T00:00:00Z"
        )
        
    except Exception as e:
        logger.error("Failed to create conversation", error=str(e))
        raise HTTPException(status_code=500, detail="Erro ao criar conversa")


@router.get("/", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    project_id: Optional[str] = None,
    status: Optional[str] = None
):
    """Listar conversas do usuário"""
    try:
        # Mock de conversas
        conversations = [
            ConversationResponse(
                id="conv-1",
                title="Análise de Processo Financeiro",
                project_id="proj-1",
                status="active",
                ai_summary="Conversa sobre automação de processos financeiros",
                extracted_requirements=[
                    {"type": "process", "name": "Conciliação bancária", "complexity": "medium"}
                ],
                confidence_score=0.85,
                created_at="2025-01-01T00:00:00Z",
                updated_at="2025-01-01T00:00:00Z"
            ),
            ConversationResponse(
                id="conv-2",
                title="Automação de RH",
                project_id="proj-2",
                status="completed",
                ai_summary="Análise de processos de recursos humanos",
                extracted_requirements=[
                    {"type": "process", "name": "Onboarding", "complexity": "low"}
                ],
                confidence_score=0.92,
                created_at="2025-01-01T00:00:00Z",
                updated_at="2025-01-01T00:00:00Z"
            )
        ]
        
        return conversations
        
    except Exception as e:
        logger.error("Failed to get conversations", error=str(e))
        raise HTTPException(status_code=500, detail="Erro ao buscar conversas")


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    """Obter conversa específica"""
    try:
        # Mock de conversa
        return ConversationResponse(
            id=conversation_id,
            title="Análise de Processo Financeiro",
            project_id="proj-1",
            status="active",
            ai_summary="Conversa sobre automação de processos financeiros",
            extracted_requirements=[
                {"type": "process", "name": "Conciliação bancária", "complexity": "medium"}
            ],
            confidence_score=0.85,
            created_at="2025-01-01T00:00:00Z",
            updated_at="2025-01-01T00:00:00Z"
        )
        
    except Exception as e:
        logger.error("Failed to get conversation", error=str(e))
        raise HTTPException(status_code=500, detail="Erro ao buscar conversa")


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(
    conversation_id: str,
    message: MessageCreate,
    current_user: User = Depends(get_current_user)
):
    """Enviar mensagem de texto para IA"""
    try:
        # Processar mensagem com IA
        ai_response = await AIService.process_text_message(
            message=message.content,
            context=message.context
        )
        
        # Criar resposta
        response_message = MessageResponse(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            type="assistant",
            content=ai_response.get("raw_response", "Erro no processamento"),
            ai_analysis=ai_response,
            created_at="2025-01-01T00:00:00Z"
        )
        
        logger.info("Message processed successfully", 
                   conversation_id=conversation_id,
                   user_id=current_user.id)
        
        return response_message
        
    except Exception as e:
        logger.error("Failed to process message", error=str(e))
        raise HTTPException(status_code=500, detail="Erro ao processar mensagem")


@router.post("/{conversation_id}/upload")
async def upload_file(
    conversation_id: str,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    """Upload e processamento de arquivo multimodal"""
    try:
        # Ler arquivo
        file_content = await file.read()
        
        # Determinar tipo de arquivo e processar
        file_type = file.content_type
        filename = file.filename
        
        if file_type.startswith("image/"):
            # Processar imagem
            ai_response = await AIService.process_image(
                image_data=file_content,
                description=description
            )
            
        elif file_type == "application/pdf":
            # Processar PDF
            pdf_text = file_content.decode('utf-8', errors='ignore')
            ai_response = await AIService.process_pdf(
                pdf_content=pdf_text,
                filename=filename
            )
            
        elif file_type.startswith("audio/"):
            # Processar áudio
            ai_response = await AIService.process_audio(
                audio_data=file_content,
                filename=filename
            )
            
        else:
            # Processar como texto
            text_content = file_content.decode('utf-8', errors='ignore')
            ai_response = await AIService.process_text_message(
                message=text_content,
                context={"filename": filename, "description": description}
            )
        
        # Criar resposta
        response = {
            "status": "success",
            "file_processed": filename,
            "file_type": file_type,
            "ai_analysis": ai_response,
            "confidence_score": ai_response.get("confidence_score", 0.0)
        }
        
        logger.info("File processed successfully", 
                   conversation_id=conversation_id,
                   filename=filename,
                   file_type=file_type)
        
        return response
        
    except Exception as e:
        logger.error("Failed to process file", error=str(e))
        raise HTTPException(status_code=500, detail="Erro ao processar arquivo")


@router.post("/{conversation_id}/analyze")
async def analyze_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    """Analisar conversa completa e extrair requisitos"""
    try:
        # Mock de análise de conversa
        analysis_result = {
            "conversation_id": conversation_id,
            "summary": "Análise completa da conversa sobre automação de processos",
            "extracted_requirements": [
                {
                    "type": "process",
                    "name": "Conciliação bancária",
                    "description": "Processo de conciliação de extratos bancários",
                    "complexity": "medium",
                    "estimated_effort": "40 horas",
                    "priority": "high"
                },
                {
                    "type": "integration",
                    "name": "SAP ERP",
                    "description": "Integração com sistema SAP",
                    "complexity": "high",
                    "estimated_effort": "80 horas",
                    "priority": "medium"
                }
            ],
            "recommended_tools": ["n8n", "Python", "Selenium"],
            "estimated_roi": "300%",
            "confidence_score": 0.87,
            "next_steps": [
                "Criar PDD detalhado",
                "Definir escopo técnico",
                "Iniciar desenvolvimento"
            ]
        }
        
        logger.info("Conversation analyzed successfully", 
                   conversation_id=conversation_id)
        
        return analysis_result
        
    except Exception as e:
        logger.error("Failed to analyze conversation", error=str(e))
        raise HTTPException(status_code=500, detail="Erro ao analisar conversa")


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    """Deletar conversa"""
    try:
        # Mock de deleção
        logger.info("Conversation deleted", 
                   conversation_id=conversation_id,
                   user_id=current_user.id)
        
        return {"status": "success", "message": "Conversa deletada com sucesso"}
        
    except Exception as e:
        logger.error("Failed to delete conversation", error=str(e))
        raise HTTPException(status_code=500, detail="Erro ao deletar conversa")


@router.post("/{conversation_id}/convert-to-project")
async def convert_to_project(
    conversation_id: str,
    current_user: User = Depends(get_current_user)
):
    """Converter conversa em projeto"""
    try:
        # Mock de conversão
        project_data = {
            "id": str(uuid.uuid4()),
            "name": f"Projeto baseado na conversa {conversation_id}",
            "description": "Projeto criado automaticamente a partir da análise de conversa",
            "conversation_id": conversation_id,
            "created_by": current_user.id,
            "status": "planning"
        }
        
        logger.info("Conversation converted to project", 
                   conversation_id=conversation_id,
                   project_id=project_data["id"])
        
        return project_data
        
    except Exception as e:
        logger.error("Failed to convert conversation to project", error=str(e))
        raise HTTPException(status_code=500, detail="Erro ao converter conversa em projeto") 