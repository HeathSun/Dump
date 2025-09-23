"""
Tool model for VAPI tools
"""

from sqlalchemy import Column, String, Text, JSON, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Tool(Base):
    __tablename__ = "tools"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    function_schema = Column(JSON, nullable=False)
    endpoint = Column(String, nullable=False)
    method = Column(String, nullable=False, default="POST")
    headers = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
