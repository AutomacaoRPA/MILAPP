"""
Endpoints para gerenciamento de conversações (Módulo 1 - IA)
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import os
import shutil
from datetime import datetime

from ...core.database import get_db
from ...models.conversation import (
    Conversation, Message, ExtractedRequirement,
    ConversationCreate, ConversationUpdate, ConversationResponse,
    MessageCreate, MessageUpdate, MessageResponse,
    ExtractedRequirementCreate, ExtractedRequirementResponse
)
from ...models.user import User
from ...services.ai_service import AIService
from ...core.config import settings

router = APIRouter(prefix="/conversations", tags=["conversations"])

# Instância do serviço de IA
ai_service = AIService()


@router.post("/", response_model=ConversationResponse)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria uma nova conversação"""
    try:
        db_conversation = Conversation(
            project_id=conversation.project_id,
            user_id=current_user.id,
            title=conversation.title
        )
        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)
        
        return ConversationResponse.from_orm(db_conversation)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar conversação: {str(e)}")


@router.get("/", response_model=List[ConversationResponse])
def get_conversations(
    project_id: Optional[uuid.UUID] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista conversações com filtros"""
    try:
        query = db.query(Conversation)
        
        # Filtros
        if project_id:
            query = query.filter(Conversation.project_id == project_id)
        if status:
            query = query.filter(Conversation.status == status)
        
        # Apenas conversações do usuário ou projetos que tem acesso
        if current_user.role != "admin":
            query = query.filter(Conversation.user_id == current_user.id)
        
        conversations = query.offset(skip).limit(limit).all()
        
        return [ConversationResponse.from_orm(conv) for conv in conversations]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar conversações: {str(e)}")


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtém uma conversação específica"""
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversação não encontrada")
        
        # Verifica permissão
        if current_user.role != "admin" and conversation.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        return ConversationResponse.from_orm(conversation)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar conversação: {str(e)}")


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def create_message(
    conversation_id: uuid.UUID,
    message_type: str = Form(...),
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria uma nova mensagem na conversação"""
    try:
        # Verifica se a conversação existe
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversação não encontrada")
        
        # Verifica permissão
        if current_user.role != "admin" and conversation.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        # Processa arquivo se fornecido
        file_path = None
        file_size = None
        file_type = None
        
        if file:
            # Cria diretório para uploads
            upload_dir = os.path.join(settings.UPLOAD_DIR, str(conversation_id))
            os.makedirs(upload_dir, exist_ok=True)
            
            # Salva arquivo
            file_path = os.path.join(upload_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            file_size = file.size
            file_type = file.content_type
        
        # Cria mensagem do usuário
        user_message = Message(
            conversation_id=conversation_id,
            type=message_type,
            role="user",
            content=content,
            file_path=file_path,
            file_size=file_size,
            file_type=file_type
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
        
        # Processa com IA
        message_data = {
            "type": message_type,
            "content": content,
            "file_path": file_path
        }
        
        ai_result = ai_service.process_message(message_data)
        
        # Cria mensagem da IA
        ai_message = Message(
            conversation_id=conversation_id,
            type="text",
            role="assistant",
            content=ai_result.get("ai_analysis", {}).get("summary", "Processado com sucesso"),
            ai_analysis=ai_result.get("ai_analysis", {}),
            tokens_used=ai_result.get("tokens_used", 0),
            processing_time=ai_result.get("processing_time", 0),
            is_processed=ai_result.get("is_processed", True),
            error_message=ai_result.get("error_message")
        )
        db.add(ai_message)
        db.commit()
        db.refresh(ai_message)
        
        return MessageResponse.from_orm(ai_message)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao processar mensagem: {str(e)}")


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
def get_messages(
    conversation_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista mensagens de uma conversação"""
    try:
        # Verifica se a conversação existe
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversação não encontrada")
        
        # Verifica permissão
        if current_user.role != "admin" and conversation.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).offset(skip).limit(limit).all()
        
        return [MessageResponse.from_orm(msg) for msg in messages]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar mensagens: {str(e)}")


@router.post("/{conversation_id}/extract-requirements")
def extract_requirements(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Extrai requisitos de uma conversação completa"""
    try:
        # Verifica se a conversação existe
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversação não encontrada")
        
        # Verifica permissão
        if current_user.role != "admin" and conversation.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        # Extrai requisitos usando IA
        requirements = ai_service.extract_requirements_from_conversation(str(conversation_id))
        
        # Salva requisitos extraídos
        if "requirements" in requirements:
            for req_data in requirements["requirements"]:
                requirement = ExtractedRequirement(
                    conversation_id=conversation_id,
                    type=req_data["type"],
                    description=req_data["description"],
                    details=req_data.get("details", {}),
                    confidence=req_data.get("confidence", 0),
                    priority=req_data.get("priority", 0),
                    complexity=req_data.get("complexity", "low")
                )
                db.add(requirement)
            
            # Atualiza conversação
            conversation.extracted_requirements = requirements.get("requirements", [])
            conversation.confidence_score = requirements.get("confidence", 0)
            conversation.ai_summary = requirements.get("summary", "")
            
            db.commit()
        
        return {
            "requirements": requirements.get("requirements", []),
            "summary": requirements.get("summary", ""),
            "estimated_hours": requirements.get("estimated_hours", 0),
            "recommended_tools": requirements.get("recommended_tools", [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao extrair requisitos: {str(e)}")


@router.post("/{conversation_id}/generate-user-stories")
def generate_user_stories(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Gera user stories baseado nos requisitos extraídos"""
    try:
        # Verifica se a conversação existe
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversação não encontrada")
        
        # Verifica permissão
        if current_user.role != "admin" and conversation.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        # Busca requisitos extraídos
        requirements = conversation.extracted_requirements or []
        
        if not requirements:
            raise HTTPException(status_code=400, detail="Nenhum requisito encontrado. Execute extract-requirements primeiro.")
        
        # Gera user stories
        user_stories = ai_service.generate_user_stories(requirements)
        
        return user_stories
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar user stories: {str(e)}")


@router.post("/{conversation_id}/recommend-tool")
def recommend_rpa_tool(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Recomenda ferramenta RPA baseado nos requisitos"""
    try:
        # Verifica se a conversação existe
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversação não encontrada")
        
        # Verifica permissão
        if current_user.role != "admin" and conversation.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        # Busca requisitos extraídos
        requirements = conversation.extracted_requirements or []
        
        if not requirements:
            raise HTTPException(status_code=400, detail="Nenhum requisito encontrado. Execute extract-requirements primeiro.")
        
        # Recomenda ferramenta
        recommendation = ai_service.recommend_rpa_tool(requirements)
        
        return recommendation
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recomendar ferramenta: {str(e)}")


@router.put("/{conversation_id}", response_model=ConversationResponse)
def update_conversation(
    conversation_id: uuid.UUID,
    conversation_update: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza uma conversação"""
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversação não encontrada")
        
        # Verifica permissão
        if current_user.role != "admin" and conversation.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        # Atualiza campos
        update_data = conversation_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(conversation, field, value)
        
        db.commit()
        db.refresh(conversation)
        
        return ConversationResponse.from_orm(conversation)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar conversação: {str(e)}")


@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deleta uma conversação"""
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversação não encontrada")
        
        # Verifica permissão
        if current_user.role != "admin" and conversation.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        db.delete(conversation)
        db.commit()
        
        return {"message": "Conversação deletada com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar conversação: {str(e)}")


# Função auxiliar para obter usuário atual (implementar autenticação)
def get_current_user(db: Session = Depends(get_db)):
    """Função temporária para obter usuário atual"""
    # Aqui você implementaria a lógica de autenticação real
    # Por enquanto, retorna um usuário mock
    return User(
        id=uuid.uuid4(),
        email="user@example.com",
        name="Usuário Teste",
        role="stakeholder"
    )