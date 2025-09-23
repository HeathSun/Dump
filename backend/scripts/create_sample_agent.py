"""
Create sample VAPI agent
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
    """Create a sample VAPI agent"""
    load_dotenv()
    
    vapi_service = VapiService()
    
    # Sample agent configuration
    agent_config = vapi_service.create_agent_config(
        name="AI Assistant",
        model="gpt-4",
        system_prompt="You are a helpful AI assistant that can help users with various tasks. Be friendly, professional, and concise in your responses.",
        webhook_url="https://your-ngrok-subdomain.ngrok.io/webhooks/vapi"
    )
    
    try:
        print("Creating sample agent...")
        agent = await vapi_service.create_agent(agent_config)
        print(f"Agent created successfully!")
        print(f"Agent ID: {agent.get('id')}")
        print(f"Agent Name: {agent.get('name')}")
        print("\nUpdate your .env file with:")
        print(f"VAPI_AGENT_ID={agent.get('id')}")
        
    except Exception as e:
        print(f"Error creating agent: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
