"""
Call model for VAPI calls
"""

from sqlalchemy import Column, String, DateTime, Text, JSON, Boolean, Integer
from sqlalchemy.sql import func
from app.database import Base

class Call(Base):
    __tablename__ = "calls"
    
    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    status = Column(String, nullable=False, default="initiated")
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    duration = Column(Integer, nullable=True)  # in seconds
    transcript = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)
    webhook_data = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
