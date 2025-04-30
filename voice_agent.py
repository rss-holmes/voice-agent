import os
import io
import wave
import tempfile
import numpy as np
import pyaudio
import openai
import time
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
eleven_labs_voice_id = os.getenv("ELEVEN_LABS_VOICE_ID")
eleven_labs_model_id = os.getenv("ELEVEN_LABS_MODEL_ID")

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5  # Default recording time, can be adjusted

def record_audio():
    """Record audio from the microphone"""
    print("Listening... (Press Ctrl+C to stop)")
    
    audio = pyaudio.PyAudio()
    
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    
    frames = []
    
    try:
        # Start recording
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            
    except KeyboardInterrupt:
        # Stop recording on Ctrl+C
        print("\nRecording stopped.")
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Save recorded data as a WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        audio_file_path = temp_audio_file.name
        
    wf = wave.open(audio_file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return audio_file_path

def transcribe_audio(audio_file_path):
    """Transcribe audio to text using OpenAI's Whisper model"""
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcription = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            return transcription.text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def get_gpt_response(text):
    """Get response from GPT-4o for the transcribed text"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant. Be concise and conversational in your responses."},
                {"role": "user", "content": text}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting GPT response: {e}")
        return "I'm sorry, I couldn't process that request."

def text_to_speech(text):
    """Convert text to speech using ElevenLabs"""

    client = ElevenLabs(
        api_key=eleven_labs_api_key,
    )
    try:
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=eleven_labs_voice_id,
            model_id=eleven_labs_model_id,
            output_format="mp3_44100_128",
        )
        play(audio)
    except Exception as e:
        print(f"Error generating speech: {e}")
        print("Response (text only):", text)

def main():
    """Main function to run the voice agent"""
    print("Voice Agent started. Press Ctrl+C to exit the program.")
    print("Speak after 'Listening...' appears and press Ctrl+C to end your input.")
    
    try:
        while True:
            # Record audio
            audio_file_path = record_audio()
            
            # Transcribe audio
            transcript = transcribe_audio(audio_file_path)
            if not transcript:
                continue
                
            print(f"You said: {transcript}")
            
            # Get GPT response
            response = get_gpt_response(transcript)
            print(f"Assistant: {response}")
            
            # Convert response to speech
            text_to_speech(response)
            
            # Remove temporary audio file
            os.remove(audio_file_path)
            
            print("\nReady for next interaction...")
            
    except KeyboardInterrupt:
        print("\nVoice Agent stopped. Goodbye!")

if __name__ == "__main__":
    main()