"""
Logging middleware for request/response logging
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
import json

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses"""
    
    async def dispatch(self, request: Request, call_next):
        # Start time
        start_time = time.time()
        
        # Log request
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        query_params = str(request.query_params) if request.query_params else ""
        
        logger.info(
            f"Request: {method} {path} {query_params} - "
            f"Client: {client_ip} - "
            f"User-Agent: {request.headers.get('user-agent', 'unknown')}"
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            logger.info(
                f"Response: {method} {path} - "
                f"Status: {response.status_code} - "
                f"Duration: {duration:.3f}s"
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Error: {method} {path} - "
                f"Duration: {duration:.3f}s - "
                f"Error: {str(e)}",
                exc_info=True
            )
            raise
