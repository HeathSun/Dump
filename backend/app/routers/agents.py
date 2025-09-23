"""
Agent management router
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.agent import Agent
from sqlalchemy import select, update, delete

router = APIRouter()

# Pydantic models
class AgentCreate(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    model: str = "gpt-4"
    temperature: str = "0.7"
    max_tokens: str = "1000"
    voice_id: Optional[str] = None
    system_prompt: Optional[str] = None
    functions: Optional[dict] = None

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[str] = None
    max_tokens: Optional[str] = None
    voice_id: Optional[str] = None
    system_prompt: Optional[str] = None
    functions: Optional[dict] = None

class AgentResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    model: str
    temperature: str
    max_tokens: str
    voice_id: Optional[str]
    system_prompt: Optional[str]
    functions: Optional[dict]
    is_active: bool
    created_at: str
    updated_at: str

@router.post("/", response_model=AgentResponse)
async def create_agent(
    agent: AgentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new agent"""
    try:
        db_agent = Agent(**agent.dict())
        db.add(db_agent)
        await db.commit()
        await db.refresh(db_agent)
        return AgentResponse.from_orm(db_agent)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[AgentResponse])
async def get_agents(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all agents"""
    try:
        result = await db.execute(
            select(Agent).where(Agent.is_active == True).offset(skip).limit(limit)
        )
        agents = result.scalars().all()
        return [AgentResponse.from_orm(agent) for agent in agents]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific agent"""
    try:
        result = await db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        return AgentResponse.from_orm(agent)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_update: AgentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an agent"""
    try:
        update_data = agent_update.dict(exclude_unset=True)
        if update_data:
            await db.execute(
                update(Agent)
                .where(Agent.id == agent_id)
                .values(**update_data)
            )
            await db.commit()
        
        # Fetch updated agent
        result = await db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        return AgentResponse.from_orm(agent)
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete an agent (soft delete)"""
    try:
        await db.execute(
            update(Agent)
            .where(Agent.id == agent_id)
            .values(is_active=False)
        )
        await db.commit()
        return {"success": True, "message": "Agent deleted"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{agent_id}/activate")
async def activate_agent(
    agent_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Activate an agent"""
    try:
        await db.execute(
            update(Agent)
            .where(Agent.id == agent_id)
            .values(is_active=True)
        )
        await db.commit()
        return {"success": True, "message": "Agent activated"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{agent_id}/deactivate")
async def deactivate_agent(
    agent_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Deactivate an agent"""
    try:
        await db.execute(
            update(Agent)
            .where(Agent.id == agent_id)
            .values(is_active=False)
        )
        await db.commit()
        return {"success": True, "message": "Agent deactivated"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
