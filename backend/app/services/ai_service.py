"""
Serviço de IA do MILAPP para processamento multimodal
"""
import os
import time
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

# LangChain imports
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter

# OpenAI imports
import openai
from openai import OpenAI

# Processamento de arquivos
import PyPDF2
import pandas as pd
from PIL import Image
import pytesseract
import cv2
import numpy as np

# BPMN processing
import xml.etree.ElementTree as ET

from ..core.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """Serviço principal de IA para processamento multimodal"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.1,
            max_tokens=4000
        )
        
        # Configurações
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.supported_formats = {
            'text': ['.txt', '.md'],
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'pdf': ['.pdf'],
            'audio': ['.mp3', '.wav', '.m4a'],
            'bpmn': ['.bpmn', '.xml'],
            'excel': ['.xlsx', '.xls'],
            'word': ['.docx', '.doc']
        }
    
    def process_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa uma mensagem multimodal"""
        start_time = time.time()
        
        try:
            message_type = message_data.get('type', 'text')
            content = message_data.get('content', '')
            file_path = message_data.get('file_path')
            
            # Processamento baseado no tipo
            if message_type == 'text':
                analysis = self._process_text(content)
            elif message_type == 'image':
                analysis = self._process_image(file_path)
            elif message_type == 'pdf':
                analysis = self._process_pdf(file_path)
            elif message_type == 'audio':
                analysis = self._process_audio(file_path)
            elif message_type == 'bpmn':
                analysis = self._process_bpmn(file_path)
            elif message_type in ['excel', 'word']:
                analysis = self._process_document(file_path, message_type)
            else:
                analysis = {"error": f"Tipo de mensagem não suportado: {message_type}"}
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return {
                "ai_analysis": analysis,
                "processing_time": processing_time,
                "tokens_used": analysis.get("tokens_used", 0),
                "is_processed": True,
                "error_message": None
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {str(e)}")
            return {
                "ai_analysis": {"error": str(e)},
                "processing_time": int((time.time() - start_time) * 1000),
                "tokens_used": 0,
                "is_processed": False,
                "error_message": str(e)
            }
    
    def _process_text(self, text: str) -> Dict[str, Any]:
        """Processa texto e extrai requisitos"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um especialista em análise de requisitos de automação RPA.
            Analise o texto fornecido e extraia:
            1. Objetivos do processo
            2. Entradas e saídas
            3. Sistemas envolvidos
            4. Exceções e regras de negócio
            5. Stakeholders
            6. Complexidade estimada
            
            Responda em JSON com a seguinte estrutura:
            {
                "objectives": ["lista de objetivos"],
                "inputs": ["lista de entradas"],
                "outputs": ["lista de saídas"],
                "systems": ["sistemas envolvidos"],
                "exceptions": ["exceções identificadas"],
                "stakeholders": ["stakeholders"],
                "complexity": "low/medium/high",
                "estimated_hours": 0,
                "confidence": 0-100
            }"""),
            ("human", text)
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        return json.loads(response.content)
    
    def _process_image(self, file_path: str) -> Dict[str, Any]:
        """Processa imagem com OCR e análise visual"""
        try:
            # OCR
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang='por')
            
            # Análise visual com OpenCV
            img_cv = cv2.imread(file_path)
            analysis = self._analyze_image_content(img_cv)
            
            # Processa texto extraído
            text_analysis = self._process_text(text) if text.strip() else {}
            
            return {
                "ocr_text": text,
                "visual_analysis": analysis,
                "text_analysis": text_analysis,
                "type": "image_analysis"
            }
            
        except Exception as e:
            return {"error": f"Erro ao processar imagem: {str(e)}"}
    
    def _process_pdf(self, file_path: str) -> Dict[str, Any]:
        """Processa PDF e extrai texto"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
            # Processa texto extraído
            analysis = self._process_text(text)
            analysis["source"] = "pdf"
            
            return analysis
            
        except Exception as e:
            return {"error": f"Erro ao processar PDF: {str(e)}"}
    
    def _process_audio(self, file_path: str) -> Dict[str, Any]:
        """Processa áudio com Whisper"""
        try:
            # Transcreve áudio
            with open(file_path, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            
            text = transcript.text
            
            # Análise de sentimento
            sentiment_prompt = f"""
            Analise o sentimento e tom da seguinte transcrição:
            {text}
            
            Responda em JSON:
            {{
                "sentiment": "positive/negative/neutral",
                "confidence": 0-100,
                "key_points": ["pontos principais"],
                "emotion": "emotion detected"
            }}
            """
            
            sentiment_response = self.llm.invoke([HumanMessage(content=sentiment_prompt)])
            sentiment_analysis = json.loads(sentiment_response.content)
            
            # Processa texto transcrito
            text_analysis = self._process_text(text)
            
            return {
                "transcript": text,
                "sentiment_analysis": sentiment_analysis,
                "text_analysis": text_analysis,
                "type": "audio_analysis"
            }
            
        except Exception as e:
            return {"error": f"Erro ao processar áudio: {str(e)}"}
    
    def _process_bpmn(self, file_path: str) -> Dict[str, Any]:
        """Processa arquivo BPMN"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Extrai elementos BPMN
            processes = []
            tasks = []
            gateways = []
            
            for process in root.findall('.//{http://www.omg.org/spec/BPMN/20100524/MODEL}process'):
                process_info = {
                    "id": process.get('id'),
                    "name": process.get('name'),
                    "tasks": [],
                    "gateways": []
                }
                
                # Extrai tarefas
                for task in process.findall('.//{http://www.omg.org/spec/BPMN/20100524/MODEL}task'):
                    task_info = {
                        "id": task.get('id'),
                        "name": task.get('name'),
                        "type": "task"
                    }
                    process_info["tasks"].append(task_info)
                    tasks.append(task_info)
                
                # Extrai gateways
                for gateway in process.findall('.//{http://www.omg.org/spec/BPMN/20100524/MODEL}gateway'):
                    gateway_info = {
                        "id": gateway.get('id'),
                        "name": gateway.get('name'),
                        "type": gateway.get('gatewayDirection', 'unspecified')
                    }
                    process_info["gateways"].append(gateway_info)
                    gateways.append(gateway_info)
                
                processes.append(process_info)
            
            # Análise de complexidade
            complexity = self._analyze_bpmn_complexity(processes)
            
            return {
                "processes": processes,
                "total_tasks": len(tasks),
                "total_gateways": len(gateways),
                "complexity": complexity,
                "type": "bpmn_analysis"
            }
            
        except Exception as e:
            return {"error": f"Erro ao processar BPMN: {str(e)}"}
    
    def _process_document(self, file_path: str, doc_type: str) -> Dict[str, Any]:
        """Processa documentos Excel/Word"""
        try:
            if doc_type == 'excel':
                # Lê Excel
                df = pd.read_excel(file_path)
                data_summary = {
                    "rows": len(df),
                    "columns": len(df.columns),
                    "column_names": df.columns.tolist(),
                    "data_types": df.dtypes.to_dict()
                }
                
                # Converte para texto para análise
                text = df.to_string()
                
            elif doc_type == 'word':
                # Para Word, seria necessário python-docx
                # Por simplicidade, retornamos estrutura básica
                data_summary = {
                    "type": "word_document",
                    "file_path": file_path
                }
                text = f"Documento Word: {file_path}"
            
            # Processa texto extraído
            analysis = self._process_text(text)
            analysis["document_summary"] = data_summary
            
            return analysis
            
        except Exception as e:
            return {"error": f"Erro ao processar documento: {str(e)}"}
    
    def _analyze_image_content(self, img: np.ndarray) -> Dict[str, Any]:
        """Analisa conteúdo visual da imagem"""
        try:
            # Converte para escala de cinza
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detecta bordas
            edges = cv2.Canny(gray, 50, 150)
            
            # Detecta formas
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            analysis = {
                "has_text": len(cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]) > 0,
                "contour_count": len(contours),
                "image_size": img.shape,
                "estimated_complexity": "low" if len(contours) < 10 else "medium" if len(contours) < 50 else "high"
            }
            
            return analysis
            
        except Exception as e:
            return {"error": f"Erro na análise visual: {str(e)}"}
    
    def _analyze_bpmn_complexity(self, processes: List[Dict]) -> str:
        """Analisa complexidade do BPMN"""
        total_tasks = sum(len(p["tasks"]) for p in processes)
        total_gateways = sum(len(p["gateways"]) for p in processes)
        
        if total_tasks < 5 and total_gateways < 3:
            return "low"
        elif total_tasks < 15 and total_gateways < 8:
            return "medium"
        else:
            return "high"
    
    def extract_requirements_from_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Extrai requisitos de uma conversação completa"""
        try:
            # Aqui você implementaria a lógica para buscar todas as mensagens
            # da conversação e fazer uma análise consolidada
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", """Analise toda a conversação e extraia requisitos consolidados.
                Agrupe por tipo e prioridade.
                
                Responda em JSON:
                {
                    "requirements": [
                        {
                            "type": "objective/input/output/exception/system/stakeholder",
                            "description": "descrição",
                            "priority": 1-5,
                            "complexity": "low/medium/high",
                            "confidence": 0-100
                        }
                    ],
                    "summary": "resumo geral",
                    "estimated_hours": 0,
                    "recommended_tools": ["lista de ferramentas"]
                }"""),
                ("human", "Analise a conversação completa")
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            return json.loads(response.content)
            
        except Exception as e:
            logger.error(f"Erro ao extrair requisitos: {str(e)}")
            return {"error": str(e)}
    
    def generate_user_stories(self, requirements: List[Dict]) -> List[Dict[str, Any]]:
        """Gera user stories baseado nos requisitos"""
        try:
            requirements_text = json.dumps(requirements, indent=2)
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", """Gere user stories baseado nos requisitos fornecidos.
                Use o formato: "Como [tipo de usuário], eu quero [funcionalidade] para [benefício]"
                
                Responda em JSON:
                {
                    "user_stories": [
                        {
                            "title": "título",
                            "description": "descrição completa",
                            "acceptance_criteria": ["critérios"],
                            "story_points": 1-13,
                            "priority": 1-5,
                            "business_value": 1-5
                        }
                    ]
                }"""),
                ("human", f"Requisitos: {requirements_text}")
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            return json.loads(response.content)
            
        except Exception as e:
            logger.error(f"Erro ao gerar user stories: {str(e)}")
            return {"error": str(e)}
    
    def recommend_rpa_tool(self, requirements: List[Dict]) -> Dict[str, Any]:
        """Recomenda ferramenta RPA baseado nos requisitos"""
        try:
            requirements_text = json.dumps(requirements, indent=2)
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", """Analise os requisitos e recomende a melhor ferramenta RPA.
                Considere: n8n, Python, Playwright, Selenium, SikuliX, AutoHotkey.
                
                Responda em JSON:
                {
                    "recommended_tool": "nome da ferramenta",
                    "reasoning": "justificativa",
                    "alternatives": ["alternativas"],
                    "estimated_development_time": "tempo estimado",
                    "complexity": "low/medium/high",
                    "roi_estimate": "estimativa de ROI"
                }"""),
                ("human", f"Requisitos: {requirements_text}")
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            return json.loads(response.content)
            
        except Exception as e:
            logger.error(f"Erro ao recomendar ferramenta: {str(e)}")
            return {"error": str(e)}