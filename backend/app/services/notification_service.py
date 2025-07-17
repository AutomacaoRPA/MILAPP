"""
Serviço de Notificações do MILAPP
"""

import asyncio
import json
from typing import List, Dict, Optional, Any
from datetime import datetime
import structlog

from app.core.config import settings

logger = structlog.get_logger()


class NotificationService:
    """Serviço de notificações multi-canal"""
    
    def __init__(self):
        self.smtp_client = None
        self.teams_webhook_url = settings.TEAMS_WEBHOOK_URL
        self.whatsapp_api_key = settings.WHATSAPP_API_KEY
        self.whatsapp_phone = settings.WHATSAPP_PHONE_NUMBER
        self.initialized = False
    
    @classmethod
    async def initialize(cls):
        """Inicializar serviço de notificações"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Configurar SMTP se disponível
            if settings.SMTP_HOST:
                cls.smtp_client = smtplib.SMTP(
                    settings.SMTP_HOST,
                    settings.SMTP_PORT
                )
                cls.smtp_client.starttls()
                cls.smtp_client.login(
                    settings.SMTP_USERNAME,
                    settings.SMTP_PASSWORD
                )
            
            cls.initialized = True
            logger.info("Notification Service initialized successfully")
            
        except Exception as e:
            logger.error("Notification Service initialization failed", error=str(e))
            cls.initialized = False
    
    @classmethod
    async def cleanup(cls):
        """Limpar recursos do serviço de notificações"""
        try:
            if cls.smtp_client:
                cls.smtp_client.quit()
            logger.info("Notification Service cleaned up")
        except Exception as e:
            logger.error("Notification Service cleanup failed", error=str(e))
    
    @classmethod
    async def check_health(cls) -> bool:
        """Verificar saúde do serviço de notificações"""
        try:
            if not cls.initialized:
                return False
            
            # Testar SMTP se configurado
            if cls.smtp_client:
                cls.smtp_client.noop()
            
            return True
            
        except Exception as e:
            logger.error("Notification Service health check failed", error=str(e))
            return False
    
    @classmethod
    async def send_email(
        cls,
        to_email: str,
        subject: str,
        message: str,
        html_content: str = None,
        attachments: List[Dict] = None
    ) -> Dict:
        """Enviar email"""
        try:
            if not cls.smtp_client:
                raise Exception("SMTP not configured")
            
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email.mime.base import MIMEBase
            from email import encoders
            
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = settings.SMTP_USERNAME
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Adicionar corpo da mensagem
            if html_content:
                msg.attach(MIMEText(html_content, 'html'))
            else:
                msg.attach(MIMEText(message, 'plain'))
            
            # Adicionar anexos se houver
            if attachments:
                for attachment in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment['data'])
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {attachment["filename"]}'
                    )
                    msg.attach(part)
            
            # Enviar email
            cls.smtp_client.send_message(msg)
            
            logger.info("Email sent successfully", 
                       to_email=to_email,
                       subject=subject)
            
            return {
                "status": "success",
                "channel": "email",
                "recipient": to_email,
                "sent_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("Email sending failed", 
                        error=str(e),
                        to_email=to_email,
                        subject=subject)
            
            return {
                "status": "error",
                "channel": "email",
                "error": str(e),
                "recipient": to_email
            }
    
    @classmethod
    async def send_teams_message(
        cls,
        title: str,
        message: str,
        webhook_url: str = None,
        color: str = "0076D7"
    ) -> Dict:
        """Enviar mensagem para Microsoft Teams"""
        try:
            import httpx
            
            webhook_url = webhook_url or cls.teams_webhook_url
            if not webhook_url:
                raise Exception("Teams webhook URL not configured")
            
            # Criar payload do Teams
            payload = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": color,
                "title": title,
                "text": message,
                "sections": [
                    {
                        "activityTitle": "MILAPP Notification",
                        "activitySubtitle": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                        "activityImage": "https://milapp.company.com/logo.png"
                    }
                ]
            }
            
            # Enviar para Teams
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    webhook_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    logger.info("Teams message sent successfully", 
                               title=title,
                               webhook_url=webhook_url)
                    
                    return {
                        "status": "success",
                        "channel": "teams",
                        "webhook_url": webhook_url,
                        "sent_at": datetime.utcnow().isoformat()
                    }
                else:
                    raise Exception(f"Teams API returned status {response.status_code}")
                    
        except Exception as e:
            logger.error("Teams message sending failed", 
                        error=str(e),
                        title=title,
                        webhook_url=webhook_url)
            
            return {
                "status": "error",
                "channel": "teams",
                "error": str(e),
                "webhook_url": webhook_url
            }
    
    @classmethod
    async def send_whatsapp_message(
        cls,
        phone_number: str,
        message: str,
        api_key: str = None
    ) -> Dict:
        """Enviar mensagem WhatsApp"""
        try:
            import httpx
            
            api_key = api_key or cls.whatsapp_api_key
            if not api_key:
                raise Exception("WhatsApp API key not configured")
            
            # Configurar payload para WhatsApp Business API
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "text",
                "text": {
                    "body": message
                }
            }
            
            # Enviar via WhatsApp Business API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://graph.facebook.com/v17.0/{cls.whatsapp_phone}/messages",
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                )
                
                if response.status_code == 200:
                    logger.info("WhatsApp message sent successfully", 
                               phone_number=phone_number)
                    
                    return {
                        "status": "success",
                        "channel": "whatsapp",
                        "phone_number": phone_number,
                        "sent_at": datetime.utcnow().isoformat()
                    }
                else:
                    raise Exception(f"WhatsApp API returned status {response.status_code}")
                    
        except Exception as e:
            logger.error("WhatsApp message sending failed", 
                        error=str(e),
                        phone_number=phone_number)
            
            return {
                "status": "error",
                "channel": "whatsapp",
                "error": str(e),
                "phone_number": phone_number
            }
    
    @classmethod
    async def send_notification(
        cls,
        notification_type: str,
        recipients: List[str],
        subject: str,
        message: str,
        channels: List[str] = None,
        priority: str = "normal"
    ) -> Dict:
        """Enviar notificação multi-canal"""
        try:
            channels = channels or ["email"]
            results = []
            
            for channel in channels:
                if channel == "email":
                    for recipient in recipients:
                        result = await cls.send_email(
                            to_email=recipient,
                            subject=subject,
                            message=message
                        )
                        results.append(result)
                
                elif channel == "teams":
                    result = await cls.send_teams_message(
                        title=subject,
                        message=message
                    )
                    results.append(result)
                
                elif channel == "whatsapp":
                    for recipient in recipients:
                        result = await cls.send_whatsapp_message(
                            phone_number=recipient,
                            message=f"{subject}\n\n{message}"
                        )
                        results.append(result)
            
            # Resumo dos resultados
            successful = [r for r in results if r["status"] == "success"]
            failed = [r for r in results if r["status"] == "error"]
            
            summary = {
                "total_sent": len(successful),
                "total_failed": len(failed),
                "channels_used": channels,
                "results": results,
                "sent_at": datetime.utcnow().isoformat()
            }
            
            logger.info("Multi-channel notification sent", 
                       summary=summary)
            
            return summary
            
        except Exception as e:
            logger.error("Multi-channel notification failed", error=str(e))
            return {
                "status": "error",
                "error": str(e),
                "sent_at": datetime.utcnow().isoformat()
            }
    
    @classmethod
    async def send_quality_gate_notification(
        cls,
        gate_type: str,
        project_name: str,
        status: str,
        approvers: List[str],
        details: str = None
    ) -> Dict:
        """Enviar notificação de Quality Gate"""
        try:
            subject = f"Quality Gate {gate_type} - {project_name}"
            
            message = f"""
            **Quality Gate {gate_type} - {project_name}**
            
            **Status:** {status}
            **Data:** {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}
            
            {f"**Detalhes:** {details}" if details else ""}
            
            **Aprovadores:** {', '.join(approvers)}
            
            Acesse o MILAPP para revisar e aprovar.
            """
            
            # Enviar para aprovadores
            result = await cls.send_notification(
                notification_type="quality_gate",
                recipients=approvers,
                subject=subject,
                message=message,
                channels=["email", "teams"],
                priority="high"
            )
            
            return result
            
        except Exception as e:
            logger.error("Quality gate notification failed", error=str(e))
            return {"status": "error", "error": str(e)}
    
    @classmethod
    async def send_project_status_notification(
        cls,
        project_name: str,
        status: str,
        team_members: List[str],
        details: str = None
    ) -> Dict:
        """Enviar notificação de status do projeto"""
        try:
            subject = f"Status do Projeto - {project_name}"
            
            message = f"""
            **Status do Projeto: {project_name}**
            
            **Novo Status:** {status}
            **Data:** {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}
            
            {f"**Detalhes:** {details}" if details else ""}
            
            Acesse o MILAPP para mais informações.
            """
            
            result = await cls.send_notification(
                notification_type="project_status",
                recipients=team_members,
                subject=subject,
                message=message,
                channels=["email", "teams"]
            )
            
            return result
            
        except Exception as e:
            logger.error("Project status notification failed", error=str(e))
            return {"status": "error", "error": str(e)}
    
    @classmethod
    async def send_automation_alert(
        cls,
        automation_name: str,
        alert_type: str,
        message: str,
        technical_team: List[str]
    ) -> Dict:
        """Enviar alerta de automação"""
        try:
            subject = f"Alerta de Automação - {automation_name}"
            
            alert_message = f"""
            **Alerta de Automação: {automation_name}**
            
            **Tipo:** {alert_type}
            **Data:** {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}
            
            **Mensagem:** {message}
            
            Ação imediata requerida.
            """
            
            result = await cls.send_notification(
                notification_type="automation_alert",
                recipients=technical_team,
                subject=subject,
                message=alert_message,
                channels=["email", "teams", "whatsapp"],
                priority="high"
            )
            
            return result
            
        except Exception as e:
            logger.error("Automation alert failed", error=str(e))
            return {"status": "error", "error": str(e)}


# Instância global do serviço
notification_service = NotificationService()