"""
Tools router for managing VAPI tools and functions
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import httpx
from app.database import get_db
from app.models.tool import Tool
from sqlalchemy import select, update
from app.config import settings

router = APIRouter()

# Pydantic models
class ToolCreate(BaseModel):
    name: str
    description: str
    function_schema: Dict[str, Any]
    endpoint: str
    method: str = "POST"
    headers: Optional[Dict[str, str]] = None

class ToolUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    function_schema: Optional[Dict[str, Any]] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    headers: Optional[Dict[str, str]] = None

class ToolResponse(BaseModel):
    id: str
    name: str
    description: str
    function_schema: Dict[str, Any]
    endpoint: str
    method: str
    headers: Optional[Dict[str, str]]
    is_active: bool
    created_at: str
    updated_at: str

class FunctionCallRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]

@router.post("/", response_model=ToolResponse)
async def create_tool(
    tool: ToolCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new tool"""
    try:
        db_tool = Tool(**tool.dict())
        db.add(db_tool)
        await db.commit()
        await db.refresh(db_tool)
        return ToolResponse.from_orm(db_tool)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ToolResponse])
async def get_tools(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all tools"""
    try:
        result = await db.execute(
            select(Tool).where(Tool.is_active == True).offset(skip).limit(limit)
        )
        tools = result.scalars().all()
        return [ToolResponse.from_orm(tool) for tool in tools]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{tool_id}", response_model=ToolResponse)
async def get_tool(
    tool_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific tool"""
    try:
        result = await db.execute(
            select(Tool).where(Tool.id == tool_id)
        )
        tool = result.scalar_one_or_none()
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
        return ToolResponse.from_orm(tool)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{tool_id}", response_model=ToolResponse)
async def update_tool(
    tool_id: str,
    tool_update: ToolUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a tool"""
    try:
        update_data = tool_update.dict(exclude_unset=True)
        if update_data:
            await db.execute(
                update(Tool)
                .where(Tool.id == tool_id)
                .values(**update_data)
            )
            await db.commit()
        
        # Fetch updated tool
        result = await db.execute(
            select(Tool).where(Tool.id == tool_id)
        )
        tool = result.scalar_one_or_none()
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
        return ToolResponse.from_orm(tool)
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{tool_id}")
async def delete_tool(
    tool_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a tool (soft delete)"""
    try:
        await db.execute(
            update(Tool)
            .where(Tool.id == tool_id)
            .values(is_active=False)
        )
        await db.commit()
        return {"success": True, "message": "Tool deleted"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/call")
async def call_tool(
    request: FunctionCallRequest,
    db: AsyncSession = Depends(get_db)
):
    """Execute a tool function"""
    try:
        # Get tool from database
        result = await db.execute(
            select(Tool).where(Tool.name == request.tool_name, Tool.is_active == True)
        )
        tool = result.scalar_one_or_none()
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
        
        # Make HTTP request to tool endpoint
        headers = tool.headers or {}
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=tool.method,
                url=tool.endpoint,
                headers=headers,
                json=request.parameters
            )
            response.raise_for_status()
            return {
                "success": True,
                "tool_name": request.tool_name,
                "result": response.json()
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/functions/schema")
async def get_functions_schema(
    db: AsyncSession = Depends(get_db)
):
    """Get all function schemas for VAPI agents"""
    try:
        result = await db.execute(
            select(Tool).where(Tool.is_active == True)
        )
        tools = result.scalars().all()
        
        functions = []
        for tool in tools:
            functions.append({
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.function_schema
            })
        
        return {"functions": functions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Predefined tools
@router.post("/weather")
async def get_weather(city: str, country: str = "US"):
    """Get weather information for a city"""
    # This would integrate with a weather API
    return {
        "city": city,
        "country": country,
        "temperature": "72°F",
        "condition": "Sunny",
        "humidity": "45%"
    }

@router.post("/calendar")
async def get_calendar_events(date: str = None):
    """Get calendar events for a date"""
    # This would integrate with a calendar API
    return {
        "date": date or "today",
        "events": [
            {"time": "9:00 AM", "title": "Team Meeting"},
            {"time": "2:00 PM", "title": "Client Call"}
        ]
    }

@router.post("/email")
async def send_email(to: str, subject: str, body: str):
    """Send an email"""
    # This would integrate with an email service
    return {
        "success": True,
        "to": to,
        "subject": subject,
        "message_id": "msg_123456"
    }

@router.post("/database")
async def query_database(query: str, table: str = None):
    """Query the database"""
    # This would execute database queries
    return {
        "query": query,
        "table": table,
        "results": [
            {"id": 1, "name": "John Doe"},
            {"id": 2, "name": "Jane Smith"}
        ]
    }
