"""
Chat service for OpenAI integration
"""

from openai import AsyncOpenAI
from typing import List, Dict, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class ChatService:
    """Service for handling chat interactions with OpenAI"""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API key not configured. Chat functionality will be limited.")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def get_response(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        model: str = None,
        session_id: str = None
    ) -> Dict[str, any]:
        """
        Get AI response from OpenAI
        
        Args:
            message: User message
            conversation_history: Previous conversation messages
            model: OpenAI model to use
            session_id: Session identifier
            
        Returns:
            Dictionary with response and metadata
        """
        if not self.client or not settings.OPENAI_API_KEY:
            # Fallback response if OpenAI is not configured
            return {
                "response": "OpenAI API key is not configured. Please set OPENAI_API_KEY environment variable.",
                "tokens_used": 0
            }
        
        model = model or settings.OPENAI_MODEL
        
        try:
            # Prepare messages for OpenAI
            messages = []
            
            # Add system message
            messages.append({
                "role": "system",
                "content": "You are a helpful AI assistant. Provide clear, concise, and accurate responses."
            })
            
            # Add conversation history
            for msg in conversation_history[-settings.MAX_HISTORY_MESSAGES:]:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=settings.OPENAI_TEMPERATURE
            )
            
            assistant_message = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else None
            
            logger.info(f"Generated response for session {session_id}, tokens: {tokens_used}")
            
            return {
                "response": assistant_message,
                "tokens_used": tokens_used
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"OpenAI API error: {str(e)}")
