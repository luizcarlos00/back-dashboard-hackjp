import httpx
from app.config import N8N_WEBHOOK_URL
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class N8NClient:
    """
    Client for calling n8n webhooks to generate personalized questions.
    """
    
    def __init__(self):
        self.webhook_url = N8N_WEBHOOK_URL
        self.timeout = 30.0  # 30 second timeout
    
    async def generate_question(
        self,
        user_nome: str,
        user_idade: int,
        user_interesses: List[str],
        user_nivel_educacional: str,
        video_title: str,
        video_description: str,
        expected_concepts: List[str]
    ) -> Optional[str]:
        """
        Call n8n webhook to generate a personalized question based on user profile and video content.
        
        Returns:
            str: Generated question text
            None: If n8n call fails (use fallback)
        """
        try:
            payload = {
                "user": {
                    "nome": user_nome,
                    "idade": user_idade,
                    "interesses": user_interesses,
                    "nivel_educacional": user_nivel_educacional
                },
                "video": {
                    "title": video_title,
                    "description": video_description,
                    "expected_concepts": expected_concepts
                }
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.webhook_url,
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # n8n should return {"question": "..."} or {"question_text": "..."}
                    question = data.get("question") or data.get("question_text")
                    
                    if question:
                        logger.info(f"Successfully generated question via n8n for user: {user_nome}")
                        return question
                    else:
                        logger.warning("n8n response missing 'question' field")
                        return None
                else:
                    logger.error(f"n8n webhook returned status {response.status_code}")
                    return None
        
        except httpx.TimeoutException:
            logger.error("n8n webhook request timed out")
            return None
        except Exception as e:
            logger.error(f"Error calling n8n webhook: {str(e)}")
            return None
    
    def get_fallback_question(self) -> str:
        """
        Return a generic fallback question if n8n fails.
        """
        return "Explique com suas próprias palavras o que você aprendeu neste vídeo."

# Global instance
n8n_client = N8NClient()

