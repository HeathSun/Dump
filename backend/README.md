# VAPI Outbound Call Backend

A powerful backend server designed specifically for **VAPI outbound calling** with advanced agent management, webhook processing, and real-time conversation handling.

## 🎯 **Primary Focus: VAPI Outbound Calls**

This backend is built specifically for making **outbound calls using VAPI** with the following core capabilities:

- **🚀 VAPI Outbound Calls**: Direct integration with VAPI API for initiating outbound calls
- **🤖 Agent Management**: Create, configure, and manage VAPI agents for outbound calling
- **📞 Phone Number Management**: Handle VAPI phone number provisioning and configuration
- **🔄 Real-time Webhooks**: Process VAPI call events, transcripts, and function calls
- **⚡ Call Control**: Start, monitor, and end outbound calls programmatically
- **🛠️ Function Tools**: Execute custom functions during VAPI conversations
- **🌐 Ngrok Integration**: Automatic webhook endpoint creation for VAPI callbacks
- **💾 Call Tracking**: Database storage of call logs, transcripts, and metadata

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database setup
│   ├── models/                # Database models
│   │   ├── __init__.py
│   │   ├── call.py           # Call model
│   │   ├── agent.py          # Agent model
│   │   └── tool.py           # Tool model
│   ├── routers/              # API routers
│   │   ├── __init__.py
│   │   ├── vapi.py           # VAPI endpoints
│   │   ├── agents.py         # Agent management
│   │   ├── tools.py          # Tools and functions
│   │   ├── webhooks.py       # Webhook handlers
│   │   └── conversation.py   # ElevenLabs conversation
│   ├── services/             # Business logic
│   │   ├── __init__.py
│   │   ├── vapi_service.py   # VAPI service
│   │   └── ngrok_service.py  # Ngrok tunnel service
│   └── utils/                # Utilities
│       ├── __init__.py
│       └── logger.py         # Logging configuration
├── scripts/                  # Utility scripts
│   ├── init_db.py           # Database initialization
│   ├── create_sample_agent.py # Create sample VAPI agent
│   └── start_call.py        # Start outbound call
├── main.py                  # Main application
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Prerequisites

### **Required for VAPI Outbound Calls:**
- **VAPI Account**: Active VAPI account with API access
- **VAPI API Key**: Valid API key from VAPI dashboard
- **VAPI Phone Number**: Provisioned phone number for outbound calling
- **VAPI Agent**: Configured agent for making calls

### **Development Requirements:**
- Python 3.8 or higher
- Virtual environment (recommended)
- Ngrok account (for webhook endpoints)
- ElevenLabs API key (optional, for enhanced voice features)

## Installation

1. **Clone the repository and navigate to backend**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Copy the example environment file:
   ```bash
   cp ../env.example .env
   ```
   
   Edit the `.env` file with your actual API keys and configuration.

## Environment Variables

### **🔑 Essential VAPI Configuration**

```env
# VAPI Core Settings (REQUIRED)
VAPI_API_KEY=your_vapi_api_key_here
VAPI_AGENT_ID=your_vapi_agent_id_here
VAPI_PHONE_NUMBER_ID=your_vapi_phone_number_id_here

# Target Phone Number for Outbound Calls
PHONE_NUMBER=+1234567890
```

### **🌐 Webhook Configuration (REQUIRED for callbacks)**

```env
# Ngrok for VAPI webhook endpoints
NGROK_AUTH_TOKEN=your_ngrok_auth_token_here
NGROK_SUBDOMAIN=your_custom_subdomain_here

# Auto-configured webhook URLs
VAPI_WEBHOOK_URL=https://your-subdomain.ngrok.io/webhooks/vapi
```

### **⚙️ Server & Database Settings**

```env
# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=True

# Database (for call tracking)
DATABASE_URL=sqlite:///./vapi_backend.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### **🔊 Optional Voice Enhancement**

```env
# ElevenLabs for enhanced voice features
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
AGENT_ID=your_elevenlabs_agent_id_here
BOYFRIEND_NAME=Agent_Name
```

## API Keys Setup

### **🎯 VAPI Setup (Primary Focus)**

1. **Create VAPI Account**
   - Visit [VAPI Dashboard](https://dashboard.vapi.ai/)
   - Sign up and verify your account

2. **Get API Key**
   - Navigate to API Keys section
   - Generate a new API key
   - Add to `.env` as `VAPI_API_KEY`

3. **Create VAPI Agent**
   - Go to Agents section
   - Create a new agent for outbound calling
   - Configure voice, model, and behavior settings
   - Copy Agent ID to `.env` as `VAPI_AGENT_ID`

4. **Provision Phone Number**
   - Go to Phone Numbers section
   - Purchase/provision a phone number for outbound calls
   - Copy Phone Number ID to `.env` as `VAPI_PHONE_NUMBER_ID`

5. **Configure Webhooks**
   - Set webhook URL to: `https://your-subdomain.ngrok.io/webhooks/vapi`
   - Enable call events, transcripts, and function calls

### **🌐 Ngrok Setup (Required for VAPI webhooks)**

1. **Create Ngrok Account**
   - Visit [Ngrok](https://ngrok.com/)
   - Sign up for free account

2. **Get Auth Token**
   - Copy your auth token from dashboard
   - Add to `.env` as `NGROK_AUTH_TOKEN`

3. **Configure Subdomain (Optional)**
   - Set a custom subdomain for consistent webhook URLs
   - Add to `.env` as `NGROK_SUBDOMAIN`

### **🔊 ElevenLabs Setup (Optional Enhancement)**

1. **Create ElevenLabs Account**
   - Visit [ElevenLabs](https://elevenlabs.io/)
   - Sign up and get API key

2. **Create Conversational Agent**
   - Create a Conversational AI agent
   - Copy Agent ID to `.env` as `AGENT_ID`

## Usage

### **🚀 Quick Start: Make VAPI Outbound Calls**

1. **Initialize Database**
   ```bash
   python scripts/init_db.py
   ```

2. **Start VAPI Backend Server**
   ```bash
   python main.py
   ```
   
   The server will automatically:
   - Start FastAPI application on `http://localhost:8000`
   - Create Ngrok tunnel for VAPI webhook endpoints
   - Configure webhook URLs for VAPI callbacks

3. **Make Your First VAPI Outbound Call**
   ```bash
   python scripts/start_call.py
   ```
   
   This will:
   - **Initiate VAPI outbound call** to the configured phone number
   - **Process real-time VAPI events** via webhooks
   - **Track call data** in the database
   - **Handle conversation flow** with your VAPI agent

### **📞 VAPI Call Management**

#### **Start Outbound Call via API**
```bash
curl -X POST "http://localhost:8000/api/v1/vapi/calls/start" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890", "agent_id": "your_agent_id"}'
```

#### **Check Call Status**
```bash
curl "http://localhost:8000/api/v1/vapi/calls/{call_id}"
```

#### **End Call**
```bash
curl -X POST "http://localhost:8000/api/v1/vapi/calls/{call_id}/end"
```

### **🤖 VAPI Agent Management**

#### **Create New VAPI Agent**
```bash
curl -X POST "http://localhost:8000/api/v1/vapi/agents" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sales Agent",
    "model": "gpt-4",
    "voice_id": "your_voice_id",
    "system_prompt": "You are a helpful sales assistant."
  }'
```

#### **Update Agent Configuration**
```bash
curl -X PATCH "http://localhost:8000/api/v1/vapi/agents/{agent_id}" \
  -H "Content-Type: application/json" \
  -d '{"system_prompt": "Updated prompt"}'
```

## API Endpoints

### **🎯 Core VAPI Endpoints**

#### **VAPI Agent Management**
- `POST /api/v1/vapi/agents` - Create new VAPI agent
- `GET /api/v1/vapi/agents/{agent_id}` - Get agent configuration
- `PATCH /api/v1/vapi/agents/{agent_id}` - Update agent settings
- `DELETE /api/v1/vapi/agents/{agent_id}` - Delete agent

#### **VAPI Outbound Call Control**
- `POST /api/v1/vapi/calls/start` - **Start outbound call**
- `GET /api/v1/vapi/calls/{call_id}` - Get call status and details
- `POST /api/v1/vapi/calls/{call_id}/end` - End active call

#### **VAPI Phone Number Management**
- `POST /api/v1/vapi/phone-numbers` - Provision new phone number
- `GET /api/v1/vapi/phone-numbers` - List all phone numbers

### **🔄 VAPI Webhook Endpoints**

#### **Real-time VAPI Event Processing**
- `POST /webhooks/vapi` - **Main VAPI webhook handler**
- `POST /webhooks/vapi/function-call` - VAPI function call webhook
- `GET /webhooks/health` - Webhook system health check

### **🛠️ VAPI Function Tools**

#### **Custom Function Execution**
- `POST /api/v1/tools/` - Create custom function tool
- `GET /api/v1/tools/` - List all available tools
- `POST /api/v1/tools/call` - Execute function during call
- `GET /api/v1/tools/functions/schema` - Get VAPI function schemas

### **📊 Call Tracking & Analytics**

#### **Database Management**
- `GET /api/v1/agents/` - List all agents
- `GET /api/v1/agents/{agent_id}` - Get agent details
- `PATCH /api/v1/agents/{agent_id}` - Update agent configuration

## **🔄 VAPI Webhook Configuration**

The backend automatically creates Ngrok tunnels and configures webhook URLs for VAPI:

### **Auto-Configured Webhook URLs:**
1. **Main VAPI Webhook**: `https://your-subdomain.ngrok.io/webhooks/vapi`
2. **Function Call Webhook**: `https://your-subdomain.ngrok.io/webhooks/vapi/function-call`

### **Configure in VAPI Dashboard:**
1. Go to your VAPI agent settings
2. Set webhook URL to: `https://your-subdomain.ngrok.io/webhooks/vapi`
3. Enable these webhook events:
   - `call-started`
   - `call-ended`
   - `transcript`
   - `function-call`
   - `speech-update`

## **📞 VAPI Outbound Call Flow**

### **Complete Call Lifecycle:**

1. **🚀 Call Initiation**
   - Backend calls VAPI API to start outbound call
   - VAPI dials the target phone number
   - Call is established with your VAPI agent

2. **🔄 Real-time Webhook Processing**
   - VAPI sends webhook events to your backend
   - Call status, transcripts, and function calls are processed
   - All call data is stored in the database

3. **🤖 Agent Interaction**
   - VAPI agent handles the conversation
   - Custom functions can be executed during the call
   - Real-time transcript updates are captured

4. **📊 Call Tracking**
   - Complete call logs are maintained
   - Transcripts are stored for analysis
   - Call metadata and duration are tracked

5. **🛑 Call Termination**
   - Call can be ended programmatically
   - Final webhook events are processed
   - Call summary is stored in database

## Development

### **🛠️ Adding VAPI Function Tools**

1. **Create Function Endpoint**
   ```python
   # In app/routers/tools.py
   @router.post("/custom-function")
   async def custom_function(param1: str, param2: int):
       # Your function logic here
       return {"result": "success"}
   ```

2. **Register with VAPI Agent**
   ```python
   # Function schema for VAPI
   function_schema = {
       "name": "custom_function",
       "description": "Custom function for VAPI calls",
       "parameters": {
           "type": "object",
           "properties": {
               "param1": {"type": "string"},
               "param2": {"type": "integer"}
           }
       }
   }
   ```

3. **Update Agent Configuration**
   - Add function to your VAPI agent via API or dashboard
   - Function will be available during outbound calls

### **🔄 Custom VAPI Webhook Handlers**

Extend webhook processing for additional VAPI events:

```python
# In app/routers/webhooks.py
@router.post("/vapi/custom-event")
async def handle_custom_vapi_event(request: Request):
    webhook_data = await request.json()
    event_type = webhook_data.get("type")
    
    if event_type == "custom-event":
        # Handle custom VAPI event
        await process_custom_event(webhook_data)
    
    return {"success": True}
```

### **📊 Custom Call Tracking**

Add new database models for enhanced call tracking:

```python
# In app/models/
class CallAnalytics(Base):
    __tablename__ = "call_analytics"
    
    call_id = Column(String, ForeignKey("calls.id"))
    sentiment_score = Column(Float)
    keywords = Column(JSON)
    # Add your custom fields
```

## Troubleshooting

### **🚨 Common VAPI Issues**

1. **"VAPI_API_KEY not set"**
   - Ensure your `.env` file contains a valid VAPI API key
   - Verify the API key has proper permissions for outbound calls

2. **"VAPI agent not found"**
   - Check that `VAPI_AGENT_ID` matches an existing agent in your VAPI dashboard
   - Ensure the agent is properly configured for outbound calling

3. **"Phone number not provisioned"**
   - Verify `VAPI_PHONE_NUMBER_ID` is correct
   - Ensure the phone number is active and can make outbound calls

4. **"Webhook not receiving VAPI events"**
   - Check that webhook URL is correctly configured in VAPI dashboard
   - Verify Ngrok tunnel is active: `https://your-subdomain.ngrok.io/webhooks/vapi`
   - Test webhook endpoint: `curl -X POST https://your-subdomain.ngrok.io/webhooks/test`

5. **"Call failed to start"**
   - Verify target phone number format (include country code: +1234567890)
   - Check VAPI account has sufficient credits for outbound calls
   - Ensure agent has proper voice and model configuration

### **🔧 Technical Issues**

6. **Ngrok tunnel failed**
   - Verify your `NGROK_AUTH_TOKEN` is correct
   - Check that Ngrok is not already running on the same port
   - Try using a different subdomain

7. **Database connection error**
   - Ensure the database URL is correct in `.env`
   - Run the database initialization script: `python scripts/init_db.py`

8. **Function tools not working**
   - Verify function schemas are properly formatted
   - Check that functions are registered with the VAPI agent
   - Test function endpoints independently

### **📋 Debugging Steps**

1. **Check VAPI Dashboard**
   - Verify agent configuration
   - Check call logs for error details
   - Ensure webhook URL is set correctly

2. **Test Webhook Endpoints**
   ```bash
   curl -X POST "https://your-subdomain.ngrok.io/webhooks/test" \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```

3. **Monitor Logs**
   ```bash
   # Real-time log monitoring
   tail -f logs/app.log
   
   # Or check console output
   python main.py
   ```

4. **Verify API Keys**
   ```bash
   # Test VAPI connection
   curl -H "Authorization: Bearer YOUR_VAPI_API_KEY" \
     "https://api.vapi.ai/agent"
   ```

## Production Deployment

### **🚀 Production VAPI Setup**

1. **Environment Configuration**
   - Set all required VAPI environment variables
   - Use production database (PostgreSQL recommended)
   - Configure secure webhook endpoints

2. **VAPI Production Settings**
   - Use production VAPI API keys
   - Configure production phone numbers
   - Set up proper webhook URLs (not Ngrok for production)

3. **Security & Monitoring**
   - Configure proper CORS and authentication
   - Set up comprehensive logging and monitoring
   - Use HTTPS for all webhook endpoints

4. **Scaling Considerations**
   - Implement database connection pooling
   - Set up Redis for session management
   - Configure load balancing for high call volumes

## **🎯 VAPI Use Cases**

This backend is perfect for:

- **📞 Outbound Sales Calls**: Automated sales outreach
- **📋 Appointment Scheduling**: Automated booking calls
- **📢 Marketing Campaigns**: Mass outbound calling
- **🎯 Lead Qualification**: Automated lead screening
- **📞 Customer Support**: Proactive support calls
- **📊 Survey Collection**: Automated data collection calls

## License

This project is designed for VAPI outbound calling applications.

## Support

For VAPI-specific issues:
1. Check the troubleshooting section above
2. Review [VAPI Documentation](https://docs.vapi.ai/)
3. Verify all VAPI environment variables are properly set
4. Test webhook endpoints and call flows
