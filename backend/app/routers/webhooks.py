"""
Webhooks router for handling VAPI webhooks
"""

from fastapi import APIRouter, Request, HTTPException, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
import json
import logging
from app.database import get_db
from app.models.call import Call
from sqlalchemy import select, update
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/vapi")
async def vapi_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Handle VAPI webhooks"""
    try:
        # Get raw body
        body = await request.body()
        webhook_data = json.loads(body)
        
        logger.info(f"Received VAPI webhook: {webhook_data}")
        
        # Process webhook in background
        background_tasks.add_task(process_vapi_webhook, webhook_data, db)
        
        return {"success": True, "message": "Webhook received"}
        
    except Exception as e:
        logger.error(f"Error processing VAPI webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_vapi_webhook(webhook_data: Dict[str, Any], db: AsyncSession):
    """Process VAPI webhook data"""
    try:
        event_type = webhook_data.get("type")
        call_data = webhook_data.get("call", {})
        call_id = call_data.get("id")
        
        if not call_id:
            logger.warning("No call ID in webhook data")
            return
        
        # Check if call exists in database
        result = await db.execute(
            select(Call).where(Call.id == call_id)
        )
        call_record = result.scalar_one_or_none()
        
        if not call_record:
            # Create new call record
            call_record = Call(
                id=call_id,
                agent_id=call_data.get("assistantId", ""),
                phone_number=call_data.get("customer", {}).get("number", ""),
                status=call_data.get("status", "initiated"),
                metadata=call_data,
                webhook_data=webhook_data
            )
            db.add(call_record)
        else:
            # Update existing call record
            update_data = {
                "status": call_data.get("status", call_record.status),
                "webhook_data": webhook_data,
                "updated_at": datetime.utcnow()
            }
            
            # Handle specific event types
            if event_type == "call-started":
                update_data["started_at"] = datetime.utcnow()
                update_data["is_active"] = True
            elif event_type == "call-ended":
                update_data["ended_at"] = datetime.utcnow()
                update_data["is_active"] = False
                if call_record.started_at:
                    duration = (datetime.utcnow() - call_record.started_at).total_seconds()
                    update_data["duration"] = int(duration)
            elif event_type == "transcript":
                transcript = webhook_data.get("transcript", "")
                if transcript:
                    update_data["transcript"] = transcript
            
            await db.execute(
                update(Call)
                .where(Call.id == call_id)
                .values(**update_data)
            )
        
        await db.commit()
        logger.info(f"Processed webhook for call {call_id}, event: {event_type}")
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error processing webhook: {str(e)}")

@router.post("/vapi/function-call")
async def vapi_function_call_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Handle VAPI function call webhooks"""
    try:
        body = await request.body()
        webhook_data = json.loads(body)
        
        logger.info(f"Received function call webhook: {webhook_data}")
        
        # Process function call in background
        background_tasks.add_task(process_function_call, webhook_data, db)
        
        return {"success": True, "message": "Function call webhook received"}
        
    except Exception as e:
        logger.error(f"Error processing function call webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_function_call(webhook_data: Dict[str, Any], db: AsyncSession):
    """Process function call webhook"""
    try:
        call_id = webhook_data.get("callId")
        function_name = webhook_data.get("functionName")
        parameters = webhook_data.get("parameters", {})
        
        logger.info(f"Processing function call: {function_name} for call {call_id}")
        
        # Here you would implement the actual function logic
        # For now, we'll just log it
        result = {
            "function_name": function_name,
            "parameters": parameters,
            "result": "Function executed successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Function call result: {result}")
        
    except Exception as e:
        logger.error(f"Error processing function call: {str(e)}")

@router.get("/health")
async def webhook_health():
    """Webhook health check"""
    return {
        "status": "healthy",
        "service": "webhooks",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/test")
async def test_webhook(request: Request):
    """Test webhook endpoint"""
    try:
        body = await request.body()
        data = json.loads(body) if body else {}
        
        logger.info(f"Test webhook received: {data}")
        
        return {
            "success": True,
            "message": "Test webhook received",
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in test webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
