import os
from contextlib import asynccontextmanager
from tempfile import NamedTemporaryFile
from typing import Union
import warnings
from fastapi import FastAPI, File, UploadFile, HTTPException
# from openai import OpenAI
import whisper
# client = OpenAI()
import torch
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Usando dispositivo: {device}")
    ml_models['whisper'] = whisper.load_model("large", device=device)
    print('model whisper load successfully')
    yield
    print('error load model')
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}
## Whisper
@app.post('/sst-whisper')
def get_transcribe(audio: UploadFile = File(...), language: str = 'en'):
    try:
        # Guardar archivo subido en un archivo temporal
        with NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write( audio.file.read())
            temp_file_path = temp_file.name
        transcription = ml_models['whisper'].transcribe(
            audio=temp_file_path, 
            language=language, 
            verbose=False
        )
        os.remove(temp_file_path)
        return {'Transcript': transcription.get('text', '')}
    except Exception as e:
        print(f"Error en transcripción: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")
## Open AI
# @app.post('/sst')
# def get_transcribe(audio: File, language: str = 'en'):
#     transcription = client.audio.transcriptions.create(
#        model="whisper-1", file=audio, language='en')
#     print(transcription.text)
#     return {'Transcript': transcription}