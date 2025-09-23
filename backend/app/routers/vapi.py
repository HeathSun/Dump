"""
VAPI router for agent and call management
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.services.vapi_service import VapiService

router = APIRouter()

# Pydantic models
class AgentCreateRequest(BaseModel):
    name: str
    model: str = "gpt-4"
    voice_id: Optional[str] = None
    system_prompt: Optional[str] = None
    functions: Optional[List[Dict]] = None
    webhook_url: Optional[str] = None

class AgentUpdateRequest(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    voice_id: Optional[str] = None
    system_prompt: Optional[str] = None
    functions: Optional[List[Dict]] = None
    webhook_url: Optional[str] = None

class CallStartRequest(BaseModel):
    phone_number: str
    agent_id: Optional[str] = None

class PhoneNumberCreateRequest(BaseModel):
    number: str
    provider: str = "twilio"
    webhook_url: Optional[str] = None

# Dependency
def get_vapi_service() -> VapiService:
    return VapiService()

@router.post("/agents")
async def create_agent(
    request: AgentCreateRequest,
    vapi_service: VapiService = Depends(get_vapi_service)
):
    """Create a new VAPI agent"""
    try:
        agent_config = vapi_service.create_agent_config(
            name=request.name,
            model=request.model,
            voice_id=request.voice_id,
            system_prompt=request.system_prompt,
            functions=request.functions,
            webhook_url=request.webhook_url
        )
        
        agent = await vapi_service.create_agent(agent_config)
        return {"success": True, "agent": agent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/{agent_id}")
async def get_agent(
    agent_id: str,
    vapi_service: VapiService = Depends(get_vapi_service)
):
    """Get agent details"""
    try:
        agent = await vapi_service.get_agent(agent_id)
        return {"success": True, "agent": agent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/agents/{agent_id}")
async def update_agent(
    agent_id: str,
    request: AgentUpdateRequest,
    vapi_service: VapiService = Depends(get_vapi_service)
):
    """Update an agent"""
    try:
        update_data = request.dict(exclude_unset=True)
        agent = await vapi_service.update_agent(agent_id, update_data)
        return {"success": True, "agent": agent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/agents/{agent_id}")
async def delete_agent(
    agent_id: str,
    vapi_service: VapiService = Depends(get_vapi_service)
):
    """Delete an agent"""
    try:
        await vapi_service.delete_agent(agent_id)
        return {"success": True, "message": "Agent deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calls/start")
async def start_call(
    request: CallStartRequest,
    vapi_service: VapiService = Depends(get_vapi_service)
):
    """Start a new call"""
    try:
        call = await vapi_service.start_call(
            phone_number=request.phone_number,
            agent_id=request.agent_id
        )
        return {"success": True, "call": call}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/calls/{call_id}")
async def get_call(
    call_id: str,
    vapi_service: VapiService = Depends(get_vapi_service)
):
    """Get call details"""
    try:
        call = await vapi_service.get_call(call_id)
        return {"success": True, "call": call}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calls/{call_id}/end")
async def end_call(
    call_id: str,
    vapi_service: VapiService = Depends(get_vapi_service)
):
    """End a call"""
    try:
        result = await vapi_service.end_call(call_id)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/phone-numbers")
async def create_phone_number(
    request: PhoneNumberCreateRequest,
    vapi_service: VapiService = Depends(get_vapi_service)
):
    """Create a new phone number"""
    try:
        phone_config = {
            "number": request.number,
            "provider": request.provider,
            "webhookUrl": request.webhook_url
        }
        
        phone_number = await vapi_service.create_phone_number(phone_config)
        return {"success": True, "phone_number": phone_number}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/phone-numbers")
async def get_phone_numbers(
    vapi_service: VapiService = Depends(get_vapi_service)
):
    """Get all phone numbers"""
    try:
        phone_numbers = await vapi_service.get_phone_numbers()
        return {"success": True, "phone_numbers": phone_numbers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
