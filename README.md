# Voice Agent

A Python-based voice agent that uses:
- OpenAI Whisper for speech-to-text
- OpenAI GPT-4o for inference
- ElevenLabs for text-to-speech

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your API keys:
   ```
   cp .env.example .env
   ```
4. Edit the `.env` file with your actual API keys and voice ID

## Usage

Run the script:
```
python voice_agent.py
```

- Speak after seeing "Listening..." in the console
- Press Ctrl+C to stop recording your voice input
- The agent will transcribe your speech, process it with GPT-4o, and speak back using ElevenLabs

## Requirements

- Python 3.8+
- OpenAI API key
- ElevenLabs API key and a voice ID
- Microphone and speakers