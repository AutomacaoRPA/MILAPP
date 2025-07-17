"""
Endpoints para gerenciamento de Quality Gates
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
import uuid

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/")
async def get_quality_gates(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Listar quality gates"""
    try:
        # Mock data para demonstração
        quality_gates = [
            {
                "id": "qg-001",
                "name": "Validação de Dados - Automação RH",
                "project_id": "proj-001",
                "project_name": "Automação RH",
                "type": "data_validation",
                "status": "passed",
                "created_at": "2025-01-15T10:30:00Z",
                "executed_at": "2025-01-15T11:00:00Z",
                "executed_by": "João Silva",
                "score": 95,
                "threshold": 90
            },
            {
                "id": "qg-002",
                "name": "Teste de Performance - Sistema Financeiro",
                "project_id": "proj-002",
                "project_name": "Automação Financeira",
                "type": "performance_test",
                "status": "failed",
                "created_at": "2025-01-14T14:20:00Z",
                "executed_at": "2025-01-14T15:00:00Z",
                "executed_by": "Maria Santos",
                "score": 75,
                "threshold": 85
            },
            {
                "id": "qg-003",
                "name": "Validação de Segurança - E-commerce",
                "project_id": "proj-003",
                "project_name": "Automação E-commerce",
                "type": "security_test",
                "status": "passed",
                "created_at": "2025-01-13T09:15:00Z",
                "executed_at": "2025-01-13T10:00:00Z",
                "executed_by": "Carlos Oliveira",
                "score": 98,
                "threshold": 90
            }
        ]
        
        # Filtrar por projeto se especificado
        if project_id:
            quality_gates = [qg for qg in quality_gates if qg["project_id"] == project_id]
            
        # Filtrar por status se especificado
        if status:
            quality_gates = [qg for qg in quality_gates if qg["status"] == status]
            
        return {
            "quality_gates": quality_gates[skip:skip + limit],
            "total": len(quality_gates),
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar quality gates: {str(e)}")

@router.get("/{quality_gate_id}")
async def get_quality_gate(
    quality_gate_id: str,
    current_user: User = Depends(get_current_user)
):
    """Obter quality gate específico"""
    try:
        # Mock data para demonstração
        quality_gate = {
            "id": quality_gate_id,
            "name": "Validação de Dados - Automação RH",
            "project_id": "proj-001",
            "project_name": "Automação RH",
            "type": "data_validation",
            "status": "passed",
            "created_at": "2025-01-15T10:30:00Z",
            "executed_at": "2025-01-15T11:00:00Z",
            "executed_by": "João Silva",
            "score": 95,
            "threshold": 90,
            "description": "Validação de integridade dos dados do processo de RH",
            "criteria": [
                {"name": "Completude dos dados", "status": "passed", "score": 100},
                {"name": "Consistência dos dados", "status": "passed", "score": 95},
                {"name": "Validação de formato", "status": "passed", "score": 90}
            ],
            "logs": [
                {"timestamp": "2025-01-15T11:00:00Z", "level": "INFO", "message": "Iniciando validação de dados"},
                {"timestamp": "2025-01-15T11:00:30Z", "level": "INFO", "message": "Validação de completude concluída"},
                {"timestamp": "2025-01-15T11:01:00Z", "level": "INFO", "message": "Validação de consistência concluída"},
                {"timestamp": "2025-01-15T11:01:30Z", "level": "INFO", "message": "Quality gate aprovado"}
            ]
        }
        
        return quality_gate
    except Exception as e:
        raise HTTPException(status_code=404, detail="Quality gate não encontrado")

@router.post("/")
async def create_quality_gate(
    name: str,
    project_id: str,
    quality_gate_type: str,
    threshold: float,
    description: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Criar novo quality gate"""
    try:
        quality_gate_id = f"qg-{uuid.uuid4().hex[:8]}"
        
        quality_gate = {
            "id": quality_gate_id,
            "name": name,
            "project_id": project_id,
            "type": quality_gate_type,
            "threshold": threshold,
            "description": description,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "created_by": current_user.name
        }
        
        return {
            "message": "Quality gate criado com sucesso",
            "quality_gate": quality_gate
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar quality gate: {str(e)}")

@router.post("/{quality_gate_id}/execute")
async def execute_quality_gate(
    quality_gate_id: str,
    current_user: User = Depends(get_current_user)
):
    """Executar quality gate"""
    try:
        # Mock de execução
        score = 95  # Simular score
        threshold = 90
        status = "passed" if score >= threshold else "failed"
        
        return {
            "message": "Quality gate executado com sucesso",
            "quality_gate_id": quality_gate_id,
            "result": {
                "score": score,
                "threshold": threshold,
                "status": status,
                "executed_at": datetime.now().isoformat(),
                "executed_by": current_user.name
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar quality gate: {str(e)}")

@router.put("/{quality_gate_id}")
async def update_quality_gate(
    quality_gate_id: str,
    name: Optional[str] = None,
    threshold: Optional[float] = None,
    description: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Atualizar quality gate"""
    try:
        # Mock de atualização
        return {
            "message": "Quality gate atualizado com sucesso",
            "quality_gate_id": quality_gate_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar quality gate: {str(e)}")

@router.delete("/{quality_gate_id}")
async def delete_quality_gate(
    quality_gate_id: str,
    current_user: User = Depends(get_current_user)
):
    """Deletar quality gate"""
    try:
        # Mock de deleção
        return {
            "message": "Quality gate deletado com sucesso",
            "quality_gate_id": quality_gate_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar quality gate: {str(e)}")

@router.get("/types")
async def get_quality_gate_types(
    current_user: User = Depends(get_current_user)
):
    """Listar tipos de quality gates disponíveis"""
    return {
        "types": [
            {"id": "data_validation", "name": "Validação de Dados"},
            {"id": "performance_test", "name": "Teste de Performance"},
            {"id": "security_test", "name": "Teste de Segurança"},
            {"id": "code_review", "name": "Revisão de Código"},
            {"id": "integration_test", "name": "Teste de Integração"},
            {"id": "user_acceptance", "name": "Teste de Aceitação do Usuário"}
        ]
    }

@router.get("/{quality_gate_id}/metrics")
async def get_quality_gate_metrics(
    quality_gate_id: str,
    current_user: User = Depends(get_current_user)
):
    """Obter métricas do quality gate"""
    try:
        # Mock de métricas
        return {
            "quality_gate_id": quality_gate_id,
            "metrics": {
                "total_executions": 15,
                "passed_executions": 12,
                "failed_executions": 3,
                "success_rate": 80.0,
                "average_score": 87.5,
                "last_execution": "2025-01-15T11:00:00Z",
                "trend": "improving"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Quality gate não encontrado") 