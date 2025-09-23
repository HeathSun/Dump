"""
Agent model for VAPI agents
"""

from sqlalchemy import Column, String, Text, JSON, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    model = Column(String, nullable=False, default="gpt-4")
    temperature = Column(String, nullable=False, default="0.7")
    max_tokens = Column(String, nullable=False, default="1000")
    voice_id = Column(String, nullable=True)
    system_prompt = Column(Text, nullable=True)
    functions = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
