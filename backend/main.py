from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import uuid
from pythaitts import TTS
import traceback
import shutil
import numpy as np
import soundfile as sf

# Create directories if they don't exist
os.makedirs("../frontend/public/audio", exist_ok=True)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextToSpeechRequest(BaseModel):
    text: str
    speed: int = 22050  # Default speed is 22050 Hz

@app.post("/api/convert-to-speech")
async def convert_to_speech(request: TextToSpeechRequest):
    try:
        # Initialize TTS engine
        tts = TTS(pretrained="lunarlist_onnx")
        
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.wav"
        output_path = f"../frontend/public/audio/{filename}"

    #    # การเซ็ตค่าแบบ กำหนดค่าเอง
    #     output_file = tts.tts(
    #         text=request.text,
    #         speaker_idx="Linda",
    #         language_idx="th-th",
    #         return_type="file",
    #         filename=output_path
    #     )
        
        # Get waveform data directly
        wave = tts.tts(text=request.text, return_type="waveform")
        
        # Save the waveform to WAV file with the requested speed (sample rate)
        sf.write(output_path, wave, request.speed)
        
        # Debugging output
        print(f"Output path: {output_path}")
        print(f"File exists: {os.path.exists(output_path)}")
        print(f"Speed (sample rate): {request.speed}")
        
        # Return the URL to the audio file
        return {"audio_url": f"/audio/{filename}"}
    except Exception as e:
        # Print detailed error information
        error_details = traceback.format_exc()
        print(f"Error converting text to speech: {str(e)}")
        print(f"Traceback: {error_details}")
        raise HTTPException(status_code=500, detail=f"Failed to convert text to speech: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)