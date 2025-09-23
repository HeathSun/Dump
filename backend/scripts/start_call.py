"""
Script to start outbound calls using VAPI and ElevenLabs Conversational AI
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.vapi_service import VapiService
from app.config import settings

async def main():
    """Start an outbound call with VAPI and ElevenLabs Conversational AI"""
    load_dotenv()
    
    vapi_service = VapiService()
    
    # Get phone number from environment or user input
    phone_number = settings.PHONE_NUMBER
    if not phone_number:
        phone_number = input("Enter phone number to call: ")
    
    if not phone_number:
        print("Phone number is required!")
        return
    
    print(f"Starting outbound call to {phone_number}")
    print(f"Agent: {settings.BOYFRIEND_NAME}")
    
    try:
        # Start VAPI outbound call
        print("\n1. Starting VAPI outbound call...")
        call_data = await vapi_service.start_outbound_call(phone_number)
        print(f"VAPI call started: {call_data}")
        
        # Start ElevenLabs conversation
        print("\n2. Starting ElevenLabs conversation...")
        conversation_data = await vapi_service.start_elevenlabs_conversation(phone_number)
        print(f"ElevenLabs conversation started: {conversation_data}")
        
        print("\n3. Both services are now active!")
        print("The VAPI agent will handle the phone call while ElevenLabs handles the conversation.")
        print("Press Ctrl+C to end the conversation...")
        
        # Keep the conversation alive
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nEnding conversation...")
            
            # End ElevenLabs conversation
            end_data = await vapi_service.end_elevenlabs_conversation()
            print(f"ElevenLabs conversation ended: {end_data}")
            
            # Note: VAPI call will end when the conversation ends
            print("Call session completed!")
        
    except Exception as e:
        print(f"Error starting call: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
