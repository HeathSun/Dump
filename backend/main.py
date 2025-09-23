"""
VAPI Backend Server
A comprehensive backend for VAPI agents with webhook handling, tools, and assistance.
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pyngrok import ngrok, conf
from dotenv import load_dotenv

from app.config import settings
from app.database import init_db
from app.routers import vapi, agents, tools, webhooks, conversation
from app.services.ngrok_service import NgrokService
from app.services.vapi_service import VapiService
from app.utils.logger import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global services
ngrok_service: Optional[NgrokService] = None
vapi_service: Optional[VapiService] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global ngrok_service, vapi_service
    
    # Startup
    logger.info("Starting VAPI Backend Server...")
    
    # Initialize database
    await init_db()
    
    # Initialize Ngrok service
    ngrok_service = NgrokService()
    await ngrok_service.start_tunnel()
    
    # Initialize VAPI service
    vapi_service = VapiService()
    
    logger.info("Server startup complete!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down server...")
    if ngrok_service:
        await ngrok_service.stop_tunnel()
    logger.info("Server shutdown complete!")

# Create FastAPI app
app = FastAPI(
    title="VAPI Backend",
    description="Backend server for VAPI agents with webhook handling and tools",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(vapi.router, prefix="/api/v1/vapi", tags=["vapi"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(tools.router, prefix="/api/v1/tools", tags=["tools"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
app.include_router(conversation.router, prefix="/api/v1/conversation", tags=["conversation"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "VAPI Backend Server",
        "version": "1.0.0",
        "status": "running",
        "webhook_url": ngrok_service.get_public_url() if ngrok_service else None
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ngrok": ngrok_service.is_running() if ngrok_service else False,
        "vapi": vapi_service.is_configured() if vapi_service else False
    }

@app.post("/api/v1/calls/start")
async def start_call(
    phone_number: str,
    agent_id: Optional[str] = None,
    background_tasks: BackgroundTasks = None
):
    """Start a new VAPI call"""
    try:
        if not vapi_service:
            raise HTTPException(status_code=500, detail="VAPI service not initialized")
        
        call_data = await vapi_service.start_call(
            phone_number=phone_number,
            agent_id=agent_id or settings.VAPI_AGENT_ID
        )
        
        logger.info(f"Call started: {call_data}")
        return {"success": True, "call": call_data}
        
    except Exception as e:
        logger.error(f"Failed to start call: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/calls/{call_id}")
async def get_call_status(call_id: str):
    """Get call status"""
    try:
        if not vapi_service:
            raise HTTPException(status_code=500, detail="VAPI service not initialized")
        
        call_data = await vapi_service.get_call(call_id)
        return {"success": True, "call": call_data}
        
    except Exception as e:
        logger.error(f"Failed to get call status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/calls/{call_id}")
async def end_call(call_id: str):
    """End a call"""
    try:
        if not vapi_service:
            raise HTTPException(status_code=500, detail="VAPI service not initialized")
        
        await vapi_service.end_call(call_id)
        return {"success": True, "message": "Call ended"}
        
    except Exception as e:
        logger.error(f"Failed to end call: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def get_ngrok_service() -> NgrokService:
    """Dependency to get ngrok service"""
    if not ngrok_service:
        raise HTTPException(status_code=500, detail="Ngrok service not available")
    return ngrok_service

def get_vapi_service() -> VapiService:
    """Dependency to get VAPI service"""
    if not vapi_service:
        raise HTTPException(status_code=500, detail="VAPI service not available")
    return vapi_service

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
