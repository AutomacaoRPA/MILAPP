"""
Endpoints para gerenciamento de documentos
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from datetime import datetime
import uuid

from app.core.database import get_session
from app.core.security import get_current_user
from app.models.user import User
from app.models.project import Project

router = APIRouter()

@router.get("/")
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[str] = None,
    document_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Listar documentos"""
    try:
        # Mock data para demonstração
        documents = [
            {
                "id": "doc-001",
                "name": "Especificação Técnica - Automação RH",
                "type": "technical_spec",
                "project_id": "proj-001",
                "project_name": "Automação RH",
                "size": "2.5 MB",
                "uploaded_at": "2025-01-15T10:30:00Z",
                "uploaded_by": "João Silva",
                "status": "approved"
            },
            {
                "id": "doc-002", 
                "name": "Manual de Usuário - Sistema Financeiro",
                "type": "user_manual",
                "project_id": "proj-002",
                "project_name": "Automação Financeira",
                "size": "1.8 MB",
                "uploaded_at": "2025-01-14T14:20:00Z",
                "uploaded_by": "Maria Santos",
                "status": "pending"
            },
            {
                "id": "doc-003",
                "name": "Relatório de Testes - E-commerce",
                "type": "test_report",
                "project_id": "proj-003", 
                "project_name": "Automação E-commerce",
                "size": "3.2 MB",
                "uploaded_at": "2025-01-13T09:15:00Z",
                "uploaded_by": "Carlos Oliveira",
                "status": "approved"
            }
        ]
        
        # Filtrar por projeto se especificado
        if project_id:
            documents = [doc for doc in documents if doc["project_id"] == project_id]
            
        # Filtrar por tipo se especificado
        if document_type:
            documents = [doc for doc in documents if doc["type"] == document_type]
            
        return {
            "documents": documents[skip:skip + limit],
            "total": len(documents),
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar documentos: {str(e)}")

@router.get("/{document_id}")
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Obter documento específico"""
    try:
        # Mock data para demonstração
        document = {
            "id": document_id,
            "name": "Especificação Técnica - Automação RH",
            "type": "technical_spec",
            "project_id": "proj-001",
            "project_name": "Automação RH",
            "size": "2.5 MB",
            "uploaded_at": "2025-01-15T10:30:00Z",
            "uploaded_by": "João Silva",
            "status": "approved",
            "description": "Documento técnico detalhando a automação do processo de RH",
            "tags": ["rpa", "rh", "automação"],
            "version": "1.0",
            "download_url": f"/api/v1/documents/{document_id}/download"
        }
        
        return document
    except Exception as e:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

@router.post("/")
async def create_document(
    name: str = Form(...),
    project_id: str = Form(...),
    document_type: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Criar novo documento"""
    try:
        # Mock de criação
        document_id = f"doc-{uuid.uuid4().hex[:8]}"
        
        document = {
            "id": document_id,
            "name": name,
            "type": document_type,
            "project_id": project_id,
            "size": f"{len(file.file.read()) / 1024 / 1024:.1f} MB",
            "uploaded_at": datetime.now().isoformat(),
            "uploaded_by": current_user.name,
            "status": "pending",
            "description": description
        }
        
        return {
            "message": "Documento criado com sucesso",
            "document": document
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar documento: {str(e)}")

@router.put("/{document_id}")
async def update_document(
    document_id: str,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Atualizar documento"""
    try:
        # Mock de atualização
        return {
            "message": "Documento atualizado com sucesso",
            "document_id": document_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar documento: {str(e)}")

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Deletar documento"""
    try:
        # Mock de deleção
        return {
            "message": "Documento deletado com sucesso",
            "document_id": document_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar documento: {str(e)}")

@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Download do documento"""
    try:
        # Mock de download
        return {
            "download_url": f"https://storage.example.com/documents/{document_id}",
            "expires_at": "2025-02-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

@router.get("/types")
async def get_document_types(
    current_user: User = Depends(get_current_user)
):
    """Listar tipos de documentos disponíveis"""
    return {
        "types": [
            {"id": "technical_spec", "name": "Especificação Técnica"},
            {"id": "user_manual", "name": "Manual do Usuário"},
            {"id": "test_report", "name": "Relatório de Testes"},
            {"id": "process_map", "name": "Mapa de Processo"},
            {"id": "sop", "name": "Procedimento Operacional Padrão"},
            {"id": "training_material", "name": "Material de Treinamento"}
        ]
    } 