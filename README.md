# Jessica: Your Agentic Bestie

**Break up smart. Slay hard.**
A voice-powered AI companion that helps users navigate breakups, manage emotions, and level up confidence with conversational guidance. Built with OpenAI, Google Gemini, Deepgram, and ElevenLabs integrations.

---

## Features

* **💬 Voice-to-Text** – Real-time speech recognition using Deepgram API
* **🤖 AI Conversation** – Supports OpenAI GPT and Google Gemini models
* **🔊 Text-to-Speech** – Natural audio responses via Deepgram TTS
* **🎙 ElevenLabs Integration** – Conversational AI with ElevenLabs agents
* **🗑 Audio Management** – Automatic cleanup of temporary audio files

---

## Project Structure

| File         | Purpose                                                 |
| ------------ | ------------------------------------------------------- |
| `main.py`    | Main conversational AI application (OpenAI/Gemini)      |
| `test.py`    | ElevenLabs Conversational AI test script                |
| `audio.py`   | Audio processing utilities for speech recognition & TTS |
| `prompt.txt` | System prompt for AI conversations                      |
| `.env`       | Environment variables (API keys)                        |

---

## Prerequisites

* Python 3.8+
* Virtual environment (recommended)
* Microphone and speakers for voice interaction

---

## Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd dumpbg
```

2. **Create & activate a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Then add your API keys in .env
```

### Required `.env` Variables

```env
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here
DG_TTS_MODEL=aura-asteria-en  # optional
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
AGENT_ID=your_elevenlabs_agent_id_here
```

---

## Usage

Sponsors & Technology Partners

Google – Powering innovation and creativity with tools and platforms that enable builders everywhere.

ElevenLabs – An AI audio research and deployment company making content universally accessible in any language and voice. Their advanced AI models generate realistic, versatile, and contextually aware speech, voices, and sound effects across 32 languages, supporting applications from audiobooks to medical training. elevenlabs.io

Morph – Middleware for coding agents that makes LLMs practical for agentic coding, powering fast, reliable, high-throughput code edits and retrieval in large codebases. morphllm.com

Toolhouse.ai – Backend-as-a-Service (BaaS) platform to build, run, and manage AI agents, simplifying deployment, memory, observability, and prompt optimization. toolhouse.ai

### Main Application (OpenAI/Gemini)

```bash
python main.py
```

* Speak into your microphone
* Receive AI responses via text-to-speech
* Enjoy natural, voice-based conversations

### ElevenLabs Test (test.py)

```bash
python test.py
```

* Connects directly to an ElevenLabs conversational agent

---

## Configuration

* **Audio Settings:** 16kHz, mono, 16-bit PCM
* **Temporary Audio Files:** Automatically cleaned up
* **AI Models:** OpenAI GPT, Google Gemini, ElevenLabs

---

## Troubleshooting

* **Module errors:**

```bash
pip install pyaudio
```

* **AGENT\_ID not set:** Ensure `.env` has a valid `AGENT_ID`
* **ElevenLabs permissions error:** API key must have `convai_write` access
* **Audio issues:** Check microphone/speaker permissions

---

## Development

* Follow existing project structure for new features
* Update `requirements.txt` for new dependencies
* Test across both OpenAI/Gemini and ElevenLabs interfaces

---

## License & Contributing

* **License:** Educational & development purposes
* **Contributing:** Fork → Feature branch → Test → Pull request

---

## Support

* Review troubleshooting section
* Check API documentation
* Ensure environment variables are correctly set

