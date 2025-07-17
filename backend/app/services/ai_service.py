"""
Serviço de IA do MILAPP
"""

import asyncio
import json
import base64
from typing import List, Dict, Optional, Any
from datetime import datetime
import structlog

from app.core.config import settings

logger = structlog.get_logger()


class AIService:
    """Serviço de IA para processamento multimodal"""
    
    def __init__(self):
        self.openai_client = None
        self.langchain_llm = None
        self.whisper_model = None
        self.initialized = False
    
    @classmethod
    async def initialize(cls):
        """Inicializar serviço de IA"""
        try:
            import openai
            from langchain_openai import ChatOpenAI
            from langchain.schema import HumanMessage, SystemMessage
            
            # Configurar cliente OpenAI
            openai.api_key = settings.OPENAI_API_KEY
            cls.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            
            # Configurar LangChain
            cls.langchain_llm = ChatOpenAI(
                model_name=settings.AI_MODEL_NAME,
                temperature=settings.AI_TEMPERATURE,
                max_tokens=settings.AI_MAX_TOKENS
            )
            
            cls.initialized = True
            logger.info("AI Service initialized successfully")
            
        except Exception as e:
            logger.error("AI Service initialization failed", error=str(e))
            cls.initialized = False
    
    @classmethod
    async def cleanup(cls):
        """Limpar recursos do serviço de IA"""
        try:
            if cls.openai_client:
                await cls.openai_client.close()
            logger.info("AI Service cleaned up")
        except Exception as e:
            logger.error("AI Service cleanup failed", error=str(e))
    
    @classmethod
    async def check_health(cls) -> bool:
        """Verificar saúde do serviço de IA"""
        try:
            if not cls.initialized:
                return False
            
            # Testar conexão com OpenAI
            response = await cls.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            
            return response is not None
            
        except Exception as e:
            logger.error("AI Service health check failed", error=str(e))
            return False
    
    @classmethod
    async def process_text_message(cls, message: str, context: Dict = None) -> Dict:
        """Processar mensagem de texto"""
        try:
            if not cls.initialized:
                raise Exception("AI Service not initialized")
            
            # Construir prompt com contexto
            system_prompt = """
            Você é um assistente especializado em automação RPA (Robotic Process Automation).
            Sua função é ajudar a identificar oportunidades de automação e extrair requisitos
            de processos de negócio.
            
            Analise a mensagem do usuário e forneça:
            1. Identificação de processos candidatos à automação
            2. Requisitos técnicos identificados
            3. Estimativa de complexidade
            4. Recomendações de ferramentas RPA
            5. Próximos passos sugeridos
            """
            
            user_prompt = f"""
            Mensagem do usuário: {message}
            
            Contexto adicional: {json.dumps(context) if context else 'Nenhum'}
            
            Por favor, analise e forneça uma resposta estruturada.
            """
            
            # Processar com OpenAI
            response = await cls.openai_client.chat.completions.create(
                model=settings.AI_MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=settings.AI_TEMPERATURE,
                max_tokens=settings.AI_MAX_TOKENS
            )
            
            ai_response = response.choices[0].message.content
            
            # Estruturar resposta
            structured_response = {
                "raw_response": ai_response,
                "automation_opportunities": cls._extract_automation_opportunities(ai_response),
                "technical_requirements": cls._extract_technical_requirements(ai_response),
                "complexity_estimate": cls._extract_complexity_estimate(ai_response),
                "tool_recommendations": cls._extract_tool_recommendations(ai_response),
                "next_steps": cls._extract_next_steps(ai_response),
                "confidence_score": cls._calculate_confidence_score(ai_response),
                "processing_timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info("Text message processed successfully", 
                       message_length=len(message),
                       confidence_score=structured_response["confidence_score"])
            
            return structured_response
            
        except Exception as e:
            logger.error("Text message processing failed", error=str(e))
            return {
                "error": str(e),
                "raw_response": "Erro no processamento da mensagem",
                "confidence_score": 0.0
            }
    
    @classmethod
    async def process_image(cls, image_data: bytes, description: str = None) -> Dict:
        """Processar imagem com análise visual"""
        try:
            if not cls.initialized:
                raise Exception("AI Service not initialized")
            
            # Converter imagem para base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Construir prompt para análise de imagem
            system_prompt = """
            Você é um especialista em análise de interfaces e processos de negócio.
            Analise a imagem fornecida e identifique:
            1. Elementos de interface (botões, campos, menus)
            2. Fluxo de processo visível
            3. Oportunidades de automação
            4. Requisitos técnicos para automação
            5. Estimativa de complexidade
            """
            
            user_prompt = f"""
            Analise esta imagem de interface/processo:
            
            Descrição adicional: {description if description else 'Nenhuma'}
            
            Forneça uma análise detalhada dos elementos visíveis e oportunidades de automação.
            """
            
            # Processar com OpenAI Vision
            response = await cls.openai_client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            vision_analysis = response.choices[0].message.content
            
            # Estruturar resposta
            structured_response = {
                "raw_response": vision_analysis,
                "ui_elements": cls._extract_ui_elements(vision_analysis),
                "process_flow": cls._extract_process_flow(vision_analysis),
                "automation_opportunities": cls._extract_automation_opportunities(vision_analysis),
                "technical_requirements": cls._extract_technical_requirements(vision_analysis),
                "complexity_estimate": cls._extract_complexity_estimate(vision_analysis),
                "confidence_score": cls._calculate_confidence_score(vision_analysis),
                "processing_timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info("Image processed successfully", 
                       image_size=len(image_data),
                       confidence_score=structured_response["confidence_score"])
            
            return structured_response
            
        except Exception as e:
            logger.error("Image processing failed", error=str(e))
            return {
                "error": str(e),
                "raw_response": "Erro no processamento da imagem",
                "confidence_score": 0.0
            }
    
    @classmethod
    async def process_pdf(cls, pdf_content: str, filename: str = None) -> Dict:
        """Processar documento PDF"""
        try:
            if not cls.initialized:
                raise Exception("AI Service not initialized")
            
            # Construir prompt para análise de PDF
            system_prompt = """
            Você é um especialista em análise de documentos de negócio.
            Analise o conteúdo do PDF e extraia:
            1. Processos de negócio descritos
            2. Requisitos funcionais e técnicos
            3. Stakeholders e responsabilidades
            4. Oportunidades de automação
            5. Critérios de aceite
            6. Estimativa de complexidade
            """
            
            user_prompt = f"""
            Analise este documento PDF:
            
            Nome do arquivo: {filename if filename else 'Documento'}
            Conteúdo: {pdf_content[:4000]}  # Limitar tamanho
            
            Extraia informações estruturadas sobre processos e requisitos.
            """
            
            # Processar com OpenAI
            response = await cls.openai_client.chat.completions.create(
                model=settings.AI_MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=settings.AI_TEMPERATURE,
                max_tokens=settings.AI_MAX_TOKENS
            )
            
            pdf_analysis = response.choices[0].message.content
            
            # Estruturar resposta
            structured_response = {
                "raw_response": pdf_analysis,
                "business_processes": cls._extract_business_processes(pdf_analysis),
                "functional_requirements": cls._extract_functional_requirements(pdf_analysis),
                "technical_requirements": cls._extract_technical_requirements(pdf_analysis),
                "stakeholders": cls._extract_stakeholders(pdf_analysis),
                "automation_opportunities": cls._extract_automation_opportunities(pdf_analysis),
                "acceptance_criteria": cls._extract_acceptance_criteria(pdf_analysis),
                "complexity_estimate": cls._extract_complexity_estimate(pdf_analysis),
                "confidence_score": cls._calculate_confidence_score(pdf_analysis),
                "processing_timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info("PDF processed successfully", 
                       filename=filename,
                       content_length=len(pdf_content),
                       confidence_score=structured_response["confidence_score"])
            
            return structured_response
            
        except Exception as e:
            logger.error("PDF processing failed", error=str(e))
            return {
                "error": str(e),
                "raw_response": "Erro no processamento do PDF",
                "confidence_score": 0.0
            }
    
    @classmethod
    async def process_audio(cls, audio_data: bytes, filename: str = None) -> Dict:
        """Processar áudio com transcrição e análise"""
        try:
            if not cls.initialized:
                raise Exception("AI Service not initialized")
            
            # Transcrição com Whisper
            transcript = await cls.openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=("audio.wav", audio_data, "audio/wav")
            )
            
            transcribed_text = transcript.text
            
            # Análise do conteúdo transcrito
            analysis_response = await cls.process_text_message(
                transcribed_text,
                context={"source": "audio", "filename": filename}
            )
            
            # Estruturar resposta
            structured_response = {
                "transcription": transcribed_text,
                "audio_analysis": analysis_response,
                "confidence_score": cls._calculate_confidence_score(transcribed_text),
                "processing_timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info("Audio processed successfully", 
                       filename=filename,
                       audio_size=len(audio_data),
                       confidence_score=structured_response["confidence_score"])
            
            return structured_response
            
        except Exception as e:
            logger.error("Audio processing failed", error=str(e))
            return {
                "error": str(e),
                "transcription": "Erro na transcrição do áudio",
                "confidence_score": 0.0
            }
    
    # Métodos auxiliares para extração de informações
    @staticmethod
    def _extract_automation_opportunities(text: str) -> List[Dict]:
        """Extrair oportunidades de automação do texto"""
        # Implementar lógica de extração
        return []
    
    @staticmethod
    def _extract_technical_requirements(text: str) -> List[Dict]:
        """Extrair requisitos técnicos do texto"""
        # Implementar lógica de extração
        return []
    
    @staticmethod
    def _extract_complexity_estimate(text: str) -> Dict:
        """Extrair estimativa de complexidade"""
        # Implementar lógica de extração
        return {"level": "medium", "score": 5}
    
    @staticmethod
    def _extract_tool_recommendations(text: str) -> List[str]:
        """Extrair recomendações de ferramentas"""
        # Implementar lógica de extração
        return ["n8n", "Python", "Playwright"]
    
    @staticmethod
    def _extract_next_steps(text: str) -> List[str]:
        """Extrair próximos passos"""
        # Implementar lógica de extração
        return ["Criar PDD", "Definir escopo", "Iniciar desenvolvimento"]
    
    @staticmethod
    def _extract_ui_elements(text: str) -> List[Dict]:
        """Extrair elementos de UI"""
        # Implementar lógica de extração
        return []
    
    @staticmethod
    def _extract_process_flow(text: str) -> Dict:
        """Extrair fluxo de processo"""
        # Implementar lógica de extração
        return {"steps": [], "decision_points": []}
    
    @staticmethod
    def _extract_business_processes(text: str) -> List[Dict]:
        """Extrair processos de negócio"""
        # Implementar lógica de extração
        return []
    
    @staticmethod
    def _extract_functional_requirements(text: str) -> List[Dict]:
        """Extrair requisitos funcionais"""
        # Implementar lógica de extração
        return []
    
    @staticmethod
    def _extract_stakeholders(text: str) -> List[Dict]:
        """Extrair stakeholders"""
        # Implementar lógica de extração
        return []
    
    @staticmethod
    def _extract_acceptance_criteria(text: str) -> List[str]:
        """Extrair critérios de aceite"""
        # Implementar lógica de extração
        return []
    
    @staticmethod
    def _calculate_confidence_score(text: str) -> float:
        """Calcular score de confiança da análise"""
        # Implementar lógica de cálculo
        return 0.8


# Instância global do serviço
ai_service = AIService() 