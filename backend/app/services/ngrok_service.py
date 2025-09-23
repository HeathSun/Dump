"""
Ngrok service for creating public tunnels
"""

import asyncio
import logging
from typing import Optional
from pyngrok import ngrok, conf
from app.config import settings

logger = logging.getLogger(__name__)

class NgrokService:
    """Service for managing Ngrok tunnels"""
    
    def __init__(self):
        self.tunnel = None
        self.public_url = None
        
    async def start_tunnel(self, port: int = None) -> str:
        """Start ngrok tunnel"""
        try:
            # Configure ngrok
            if settings.NGROK_AUTH_TOKEN:
                conf.get_default().auth_token = settings.NGROK_AUTH_TOKEN
            
            port = port or settings.SERVER_PORT
            
            # Start tunnel
            self.tunnel = ngrok.connect(
                port,
                subdomain=settings.NGROK_SUBDOMAIN,
                proto="http"
            )
            
            self.public_url = self.tunnel.public_url
            logger.info(f"Ngrok tunnel started: {self.public_url}")
            
            return self.public_url
            
        except Exception as e:
            logger.error(f"Failed to start ngrok tunnel: {str(e)}")
            raise
    
    async def stop_tunnel(self):
        """Stop ngrok tunnel"""
        try:
            if self.tunnel:
                ngrok.disconnect(self.tunnel.public_url)
                ngrok.kill()
                self.tunnel = None
                self.public_url = None
                logger.info("Ngrok tunnel stopped")
        except Exception as e:
            logger.error(f"Failed to stop ngrok tunnel: {str(e)}")
    
    def get_public_url(self) -> Optional[str]:
        """Get the public URL of the tunnel"""
        return self.public_url
    
    def is_running(self) -> bool:
        """Check if tunnel is running"""
        return self.tunnel is not None
    
    def get_webhook_url(self, path: str = "/webhooks/vapi") -> Optional[str]:
        """Get webhook URL for a specific path"""
        if self.public_url:
            return f"{self.public_url.rstrip('/')}{path}"
        return None
