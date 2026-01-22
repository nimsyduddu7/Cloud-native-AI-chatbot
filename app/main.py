"""
Production-Grade Cloud-Native AI Chatbot
Main FastAPI application with OpenAI integration
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import logging
from contextlib import asynccontextmanager

from app.middleware.rate_limiter import RateLimiter
from app.middleware.logging_middleware import LoggingMiddleware
from app.services.chat_service import ChatService
from app.services.memory_service import MemoryService
from app.config import settings
from app import metrics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting AI Chatbot application...")
    await MemoryService.initialize()
    logger.info("Application started successfully")
    yield
    # Shutdown
    logger.info("Shutting down application...")
    await MemoryService.close()
    logger.info("Application shut down")


app = FastAPI(
    title="Cloud-Native AI Chatbot",
    description="Production-grade AI chatbot with context memory, rate limiting, and monitoring",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimiter)

# Initialize services
chat_service = ChatService()
memory_service = MemoryService()


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(..., min_length=1, max_length=100)
    model: Optional[str] = Field(default="gpt-3.5-turbo", description="OpenAI model to use")


class ChatResponse(BaseModel):
    response: str
    session_id: str
    model: str
    tokens_used: Optional[int] = None


class HealthResponse(BaseModel):
    status: str
    redis_connected: bool
    openai_configured: bool


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Cloud-Native AI Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    redis_status = await memory_service.is_connected()
    openai_status = bool(settings.OPENAI_API_KEY)
    
    status = "healthy" if (redis_status and openai_status) else "degraded"
    
    return HealthResponse(
        status=status,
        redis_connected=redis_status,
        openai_configured=openai_status
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(
    chat_message: ChatMessage,
    request: Request
):
    """
    Chat endpoint - Send a message and get AI response with context memory
    """
    try:
        # Record metrics
        from app.metrics import requests_total, active_requests, responses_total, tokens_used, errors_total
        requests_total.inc()
        active_requests.inc()
        
        # Get conversation history from Redis
        history = await memory_service.get_conversation_history(
            chat_message.session_id
        )
        
        # Generate response using OpenAI
        response_data = await chat_service.get_response(
            message=chat_message.message,
            conversation_history=history,
            model=chat_message.model,
            session_id=chat_message.session_id
        )
        
        # Store conversation in Redis
        await memory_service.add_message(
            session_id=chat_message.session_id,
            role="user",
            content=chat_message.message
        )
        await memory_service.add_message(
            session_id=chat_message.session_id,
            role="assistant",
            content=response_data["response"]
        )
        
        # Update metrics
        active_requests.dec()
        responses_total.inc()
        if response_data.get("tokens_used"):
            tokens_used.observe(response_data["tokens_used"])
        
        return ChatResponse(
            response=response_data["response"],
            session_id=chat_message.session_id,
            model=chat_message.model,
            tokens_used=response_data.get("tokens_used")
        )
        
    except Exception as e:
        from app.metrics import active_requests, errors_total
        active_requests.dec()
        errors_total.inc()
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/sessions/{session_id}/history", tags=["Chat"])
async def get_history(session_id: str):
    """Get conversation history for a session"""
    try:
        history = await memory_service.get_conversation_history(session_id)
        return {
            "session_id": session_id,
            "history": history,
            "message_count": len(history)
        }
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/sessions/{session_id}", tags=["Chat"])
async def clear_session(session_id: str):
    """Clear conversation history for a session"""
    try:
        await memory_service.clear_session(session_id)
        return {"message": f"Session {session_id} cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics", tags=["Monitoring"])
async def metrics_endpoint():
    """Prometheus metrics endpoint"""
    from prometheus_client import generate_latest
    from fastapi.responses import Response
    return Response(content=generate_latest(), media_type="text/plain")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
