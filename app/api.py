from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import base64
from .speech_to_text import VAD
from .llm_response import generate_response
from .text_to_speech import load_tts_model, text_to_speech

# Create router
router = APIRouter()

# Load TTS model once
tts_model, tts_tokenizer = load_tts_model()

# Directories
os.makedirs("audio_inputs", exist_ok=True)
os.makedirs("audio_outputs", exist_ok=True)

# Text Input Model
class TextInput(BaseModel):
    text: str

# ---------- 1. TEXT INPUT ENDPOINT ---------- #
@router.post("/process_text/")
async def process_text(input_data: TextInput):
    input_text = input_data.text
    llm_response = generate_response(input_text)

    output_audio_path = f"audio_outputs/output_from_text.wav"
    text_to_speech(tts_model, tts_tokenizer, llm_response, "Friendly voice", output_audio_path)

    # Read the audio file and convert to base64
    with open(output_audio_path, "rb") as audio_file:
        audio_data = base64.b64encode(audio_file.read()).decode('utf-8')

    return {
        "Input Text": input_text,
        "LLM Response": llm_response,
        "Audio": audio_data,
        "Audio Path": f"/audio_outputs/{os.path.basename(output_audio_path)}"
    }



# ---------- 2. AUDIO FILE INPUT ENDPOINT ---------- #
@router.post("/process_audio_file/")
async def process_audio_file(file: UploadFile = File(...)):
    input_path = f"audio_inputs/{file.filename}"
    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())

    vad = VAD()
    transcription = vad.recognize_speech_from_file(input_path)
    llm_response = generate_response(transcription)

    output_audio_path = f"audio_outputs/output_from_file.wav"
    text_to_speech(tts_model, tts_tokenizer, llm_response, "Friendly voice", output_audio_path)

    # Read the audio file and convert to base64
    with open(output_audio_path, "rb") as audio_file:
        audio_data = base64.b64encode(audio_file.read()).decode('utf-8')

    return {
        "Transcription": transcription,
        "LLM Response": llm_response,
        "Audio": audio_data,
        "Audio Path": f"/audio_outputs/{os.path.basename(output_audio_path)}"
    }


# ---------- 3. REAL-TIME MIC INPUT ENDPOINT ---------- #
@router.post("/process_mic/")
async def process_mic():
    vad = VAD()
    transcription = vad.process_audio()
    llm_response = generate_response(transcription)

    output_audio_path = f"audio_outputs/output_from_mic.wav"
    text_to_speech(tts_model, tts_tokenizer, llm_response, "Friendly voice", output_audio_path)

    # Read the audio file and convert to base64
    with open(output_audio_path, "rb") as audio_file:
        audio_data = base64.b64encode(audio_file.read()).decode('utf-8')

    return {
        "Transcription": transcription,
        "LLM Response": llm_response,
        "Audio": audio_data,
        "Audio Path": f"/audio_outputs/{os.path.basename(output_audio_path)}"
    }
