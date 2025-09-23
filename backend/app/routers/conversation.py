"""
Conversation router for ElevenLabs Conversational AI
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from app.services.vapi_service import VapiService

router = APIRouter()

# Pydantic models
class ConversationStartRequest(BaseModel):
    phone_number: Optional[str] = None

class ConversationResponse(BaseModel):
    success: bool
    conversation_started: bool = False
    conversation_ended: bool = False
    agent_name: str
    phone_number: str
    conversation_id: Optional[str] = None
    message: Optional[str] = None

# Dependency
def get_vapi_service() -> VapiService:
    return VapiService()

@router.post("/elevenlabs/start", response_model=ConversationResponse)
async def start_elevenlabs_conversation(
    request: ConversationStartRequest,
    vapi_service: VapiService = Depends(get_vapi_service)
):
    """Start an ElevenLabs Conversational AI conversation"""
    try:
        result = await vapi_service.start_elevenlabs_conversation(
            phone_number=request.phone_number
        )
        return ConversationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/elevenlabs/end", response_model=ConversationResponse)
async def end_elevenlabs_conversation(
    vapi_service: VapiService = Depends(get_vapi_service)
):
    """End the active ElevenLabs conversation"""
    try:
        result = await vapi_service.end_elevenlabs_conversation()
        return ConversationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/elevenlabs/status")
async def get_conversation_status(
    vapi_service: VapiService = Depends(get_vapi_service)
):
    """Get the status of the current ElevenLabs conversation"""
    try:
        status = vapi_service.get_conversation_status()
        return {"success": True, "status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/vapi/outbound")
async def start_vapi_outbound_call(
    phone_number: str,
    agent_id: Optional[str] = None,
    vapi_service: VapiService = Depends(get_vapi_service)
):
    """Start a VAPI outbound call"""
    try:
        call_data = await vapi_service.start_outbound_call(
            phone_number=phone_number,
            agent_id=agent_id
        )
        return {"success": True, "call": call_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
