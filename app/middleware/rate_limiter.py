"""
Rate limiting middleware using Redis
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
import hashlib
import logging
from app.config import settings
from app.services.memory_service import MemoryService

logger = logging.getLogger(__name__)


class RateLimiter(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health and metrics endpoints
        if request.url.path in ["/health", "/metrics", "/docs", "/openapi.json", "/"]:
            return await call_next(request)
        
        # Get client identifier
        client_id = self._get_client_id(request)
        
        # Check rate limits
        try:
            if await MemoryService.is_connected():
                # Use Redis for distributed rate limiting
                passed = await self._check_rate_limit_redis(client_id)
            else:
                # Fallback to in-memory rate limiting
                passed = await self._check_rate_limit_memory(client_id)
            
            if not passed:
                logger.warning(f"Rate limit exceeded for client: {client_id}")
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "error": "Rate limit exceeded",
                        "message": "Too many requests. Please try again later."
                    }
                )
        except Exception as e:
            logger.error(f"Rate limiting error: {str(e)}")
            # Allow request through if rate limiting fails
            pass
        
        response = await call_next(request)
        return response
    
    def _get_client_id(self, request: Request) -> str:
        """Get unique client identifier"""
        # Use IP address or API key if available
        client_ip = request.client.host if request.client else "unknown"
        api_key = request.headers.get("X-API-Key", "")
        
        if api_key:
            return hashlib.md5(api_key.encode()).hexdigest()
        return hashlib.md5(client_ip.encode()).hexdigest()
    
    async def _check_rate_limit_redis(self, client_id: str) -> bool:
        """Check rate limit using Redis"""
        try:
            client = MemoryService._client
            if not client:
                return True
            
            now = int(time.time())
            minute_key = f"ratelimit:{client_id}:minute:{now // 60}"
            hour_key = f"ratelimit:{client_id}:hour:{now // 3600}"
            
            # Check minute limit
            minute_count = await client.incr(minute_key)
            if minute_count == 1:
                await client.expire(minute_key, 60)
            if minute_count > settings.RATE_LIMIT_PER_MINUTE:
                return False
            
            # Check hour limit
            hour_count = await client.incr(hour_key)
            if hour_count == 1:
                await client.expire(hour_key, 3600)
            if hour_count > settings.RATE_LIMIT_PER_HOUR:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Redis rate limit check error: {str(e)}")
            return True
    
    # In-memory rate limiting (fallback)
    _memory_limits: dict = {}
    
    async def _check_rate_limit_memory(self, client_id: str) -> bool:
        """Check rate limit using in-memory storage (fallback)"""
        now = time.time()
        
        if client_id not in self._memory_limits:
            self._memory_limits[client_id] = {
                "minute": {"count": 0, "window": now // 60},
                "hour": {"count": 0, "window": now // 3600}
            }
        
        limits = self._memory_limits[client_id]
        current_minute = int(now // 60)
        current_hour = int(now // 3600)
        
        # Reset if window changed
        if limits["minute"]["window"] != current_minute:
            limits["minute"] = {"count": 0, "window": current_minute}
        if limits["hour"]["window"] != current_hour:
            limits["hour"] = {"count": 0, "window": current_hour}
        
        # Increment and check
        limits["minute"]["count"] += 1
        limits["hour"]["count"] += 1
        
        if limits["minute"]["count"] > settings.RATE_LIMIT_PER_MINUTE:
            return False
        if limits["hour"]["count"] > settings.RATE_LIMIT_PER_HOUR:
            return False
        
        return True
