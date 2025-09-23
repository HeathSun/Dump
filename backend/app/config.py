"""
Configuration settings for the VAPI backend
"""

import os
from typing import Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings"""
    
    # VAPI Configuration
    VAPI_API_KEY: str = Field(..., env="VAPI_API_KEY")
    VAPI_AGENT_ID: str = Field(..., env="VAPI_AGENT_ID")
    VAPI_PHONE_NUMBER_ID: Optional[str] = Field(None, env="VAPI_PHONE_NUMBER_ID")
    
    # Server Configuration
    SERVER_HOST: str = Field("0.0.0.0", env="SERVER_HOST")
    SERVER_PORT: int = Field(8000, env="SERVER_PORT")
    DEBUG: bool = Field(False, env="DEBUG")
    
    # Ngrok Configuration
    NGROK_AUTH_TOKEN: Optional[str] = Field(None, env="NGROK_AUTH_TOKEN")
    NGROK_SUBDOMAIN: Optional[str] = Field(None, env="NGROK_SUBDOMAIN")
    
    # Database Configuration
    DATABASE_URL: str = Field("sqlite:///./vapi_backend.db", env="DATABASE_URL")
    REDIS_URL: str = Field("redis://localhost:6379", env="REDIS_URL")
    
    # Security
    SECRET_KEY: str = Field("your-secret-key-change-in-production", env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # External APIs
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")
    ELEVENLABS_API_KEY: Optional[str] = Field(None, env="ELEVENLABS_API_KEY")
    DEEPGRAM_API_KEY: Optional[str] = Field(None, env="DEEPGRAM_API_KEY")
    
    # ElevenLabs Conversational AI
    AGENT_ID: Optional[str] = Field(None, env="AGENT_ID")
    BOYFRIEND_NAME: str = Field("Unknown", env="BOYFRIEND_NAME")
    
    # Webhook URLs
    WEBHOOK_URL: Optional[str] = Field(None, env="WEBHOOK_URL")
    VAPI_WEBHOOK_URL: Optional[str] = Field(None, env="VAPI_WEBHOOK_URL")
    
    # Agent Configuration
    AGENT_NAME: str = Field("Assistant", env="AGENT_NAME")
    AGENT_VOICE_ID: Optional[str] = Field(None, env="AGENT_VOICE_ID")
    AGENT_MODEL: str = Field("gpt-4", env="AGENT_MODEL")
    AGENT_TEMPERATURE: float = Field(0.7, env="AGENT_TEMPERATURE")
    AGENT_MAX_TOKENS: int = Field(1000, env="AGENT_MAX_TOKENS")
    
    # Phone Configuration
    PHONE_NUMBER: Optional[str] = Field(None, env="PHONE_NUMBER")
    COUNTRY_CODE: str = Field("US", env="COUNTRY_CODE")
    
    # Logging
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    LOG_FILE: Optional[str] = Field(None, env="LOG_FILE")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()
