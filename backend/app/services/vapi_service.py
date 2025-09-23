"""
VAPI service for managing agents and calls with ElevenLabs Conversational AI integration
"""

import httpx
import logging
import asyncio
import signal
import sys
from typing import Dict, Any, Optional, List
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from app.config import settings

logger = logging.getLogger(__name__)

class VapiService:
    """Service for interacting with VAPI API"""
    
    def __init__(self):
        self.api_key = settings.VAPI_API_KEY
        self.base_url = "https://api.vapi.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_agent(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new VAPI agent"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/agent",
                    headers=self.headers,
                    json=agent_config
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to create agent: {str(e)}")
            raise
    
    async def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """Get agent details"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/agent/{agent_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get agent: {str(e)}")
            raise
    
    async def update_agent(self, agent_id: str, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing agent"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self.base_url}/agent/{agent_id}",
                    headers=self.headers,
                    json=agent_config
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to update agent: {str(e)}")
            raise
    
    async def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.base_url}/agent/{agent_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return True
        except Exception as e:
            logger.error(f"Failed to delete agent: {str(e)}")
            raise
    
    async def start_outbound_call(self, phone_number: str, agent_id: str = None) -> Dict[str, Any]:
        """Start a new outbound call using VAPI"""
        try:
            agent_id = agent_id or settings.VAPI_AGENT_ID
            
            call_data = {
                "phoneNumberId": settings.VAPI_PHONE_NUMBER_ID,
                "customer": {
                    "number": phone_number
                },
                "assistantId": agent_id,
                "type": "outbound"  # Explicitly set as outbound call
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/call",
                    headers=self.headers,
                    json=call_data
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to start outbound call: {str(e)}")
            raise
    
    async def start_call(self, phone_number: str, agent_id: str = None) -> Dict[str, Any]:
        """Start a new call (alias for outbound call)"""
        return await self.start_outbound_call(phone_number, agent_id)
    
    async def get_call(self, call_id: str) -> Dict[str, Any]:
        """Get call details"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/call/{call_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get call: {str(e)}")
            raise
    
    async def end_call(self, call_id: str) -> Dict[str, Any]:
        """End a call"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/call/{call_id}/end",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to end call: {str(e)}")
            raise
    
    async def create_phone_number(self, phone_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new phone number"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/phone-number",
                    headers=self.headers,
                    json=phone_config
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to create phone number: {str(e)}")
            raise
    
    async def get_phone_numbers(self) -> List[Dict[str, Any]]:
        """Get all phone numbers"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/phone-number",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get phone numbers: {str(e)}")
            raise
    
    def is_configured(self) -> bool:
        """Check if service is properly configured"""
        return bool(self.api_key)
    
    async def start_elevenlabs_conversation(self, phone_number: str = None) -> Dict[str, Any]:
        """Start an ElevenLabs Conversational AI conversation"""
        try:
            if not settings.ELEVENLABS_API_KEY or not settings.AGENT_ID:
                raise ValueError("ElevenLabs API key and Agent ID are required")
            
            logger.info(f"Starting ElevenLabs conversation for {settings.BOYFRIEND_NAME} at {phone_number or settings.PHONE_NUMBER}")
            
            # Initialize ElevenLabs client
            client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
            
            # Create conversation
            conversation = Conversation(
                client,
                settings.AGENT_ID,
                requires_auth=bool(settings.ELEVENLABS_API_KEY),
                audio_interface=DefaultAudioInterface(),
                callback_agent_response=lambda response: logger.info(f"Agent: {response}"),
                callback_agent_response_correction=lambda original, corrected: logger.info(f"Agent: {original} -> {corrected}"),
                callback_user_transcript=lambda transcript: logger.info(f"User: {transcript}"),
            )
            
            # Start session
            conversation.start_session()
            
            # Store conversation for later use
            self._active_conversation = conversation
            
            return {
                "success": True,
                "conversation_started": True,
                "agent_name": settings.BOYFRIEND_NAME,
                "phone_number": phone_number or settings.PHONE_NUMBER
            }
            
        except Exception as e:
            logger.error(f"Failed to start ElevenLabs conversation: {str(e)}")
            raise
    
    async def end_elevenlabs_conversation(self) -> Dict[str, Any]:
        """End the active ElevenLabs conversation"""
        try:
            if hasattr(self, '_active_conversation') and self._active_conversation:
                self._active_conversation.end_session()
                conversation_id = self._active_conversation.wait_for_session_end()
                self._active_conversation = None
                
                logger.info(f"ElevenLabs conversation ended. ID: {conversation_id}")
                return {
                    "success": True,
                    "conversation_ended": True,
                    "conversation_id": conversation_id
                }
            else:
                return {
                    "success": False,
                    "message": "No active conversation to end"
                }
        except Exception as e:
            logger.error(f"Failed to end ElevenLabs conversation: {str(e)}")
            raise
    
    def get_conversation_status(self) -> Dict[str, Any]:
        """Get the status of the current conversation"""
        has_active = hasattr(self, '_active_conversation') and self._active_conversation is not None
        return {
            "has_active_conversation": has_active,
            "agent_name": settings.BOYFRIEND_NAME,
            "phone_number": settings.PHONE_NUMBER
        }
    
    def create_agent_config(
        self,
        name: str,
        model: str = "gpt-4",
        voice_id: str = None,
        system_prompt: str = None,
        functions: List[Dict] = None,
        webhook_url: str = None
    ) -> Dict[str, Any]:
        """Create a standard agent configuration"""
        config = {
            "name": name,
            "model": {
                "provider": "openai",
                "model": model,
                "temperature": settings.AGENT_TEMPERATURE,
                "maxTokens": settings.AGENT_MAX_TOKENS
            },
            "voice": {
                "provider": "elevenlabs",
                "voiceId": voice_id or settings.AGENT_VOICE_ID
            },
            "systemPrompt": system_prompt or "You are a helpful AI assistant.",
            "webhookUrl": webhook_url
        }
        
        if functions:
            config["functions"] = functions
            
        return config
