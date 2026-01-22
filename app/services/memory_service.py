"""
Redis-based memory service for conversation context
"""

import redis.asyncio as redis
import json
from typing import List, Dict, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class MemoryService:
    """Service for managing conversation memory using Redis"""
    
    _client: Optional[redis.Redis] = None
    _initialized: bool = False
    
    @classmethod
    async def initialize(cls):
        """Initialize Redis connection"""
        try:
            cls._client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                db=settings.REDIS_DB,
                ssl=settings.REDIS_SSL,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            
            # Test connection
            await cls._client.ping()
            cls._initialized = True
            logger.info("Redis connection established successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            cls._initialized = False
            # Create a mock client for development
            cls._client = None
    
    @classmethod
    async def close(cls):
        """Close Redis connection"""
        if cls._client:
            await cls._client.close()
            logger.info("Redis connection closed")
    
    @classmethod
    async def is_connected(cls) -> bool:
        """Check if Redis is connected"""
        if not cls._client:
            return False
        try:
            await cls._client.ping()
            return True
        except:
            return False
    
    @classmethod
    def _get_key(cls, session_id: str) -> str:
        """Get Redis key for session"""
        return f"chat:session:{session_id}"
    
    @classmethod
    async def add_message(
        cls,
        session_id: str,
        role: str,
        content: str
    ):
        """Add a message to conversation history"""
        if not cls._client:
            logger.warning("Redis not connected, message not stored")
            return
        
        try:
            key = cls._get_key(session_id)
            message = {
                "role": role,
                "content": content
            }
            
            # Add message to list
            await cls._client.rpush(key, json.dumps(message))
            
            # Set expiration
            await cls._client.expire(key, settings.SESSION_TTL_HOURS * 3600)
            
            # Trim to max history
            await cls._client.ltrim(key, -settings.MAX_HISTORY_MESSAGES, -1)
            
        except Exception as e:
            logger.error(f"Error adding message to Redis: {str(e)}")
    
    @classmethod
    async def get_conversation_history(cls, session_id: str) -> List[Dict[str, str]]:
        """Get conversation history for a session"""
        if not cls._client:
            return []
        
        try:
            key = cls._get_key(session_id)
            messages = await cls._client.lrange(key, 0, -1)
            
            history = []
            for msg_json in messages:
                try:
                    msg = json.loads(msg_json)
                    history.append(msg)
                except json.JSONDecodeError:
                    continue
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            return []
    
    @classmethod
    async def clear_session(cls, session_id: str):
        """Clear conversation history for a session"""
        if not cls._client:
            return
        
        try:
            key = cls._get_key(session_id)
            await cls._client.delete(key)
            logger.info(f"Cleared session: {session_id}")
        except Exception as e:
            logger.error(f"Error clearing session: {str(e)}")
            raise
