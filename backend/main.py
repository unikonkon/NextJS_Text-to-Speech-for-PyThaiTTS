from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import uuid
from pythaitts import TTS
import traceback
import shutil

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

@app.post("/api/convert-to-speech")
async def convert_to_speech(request: TextToSpeechRequest):
    try:
        # Initialize TTS engine
        tts = TTS()
        
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.wav"
        output_path = f"../frontend/public/audio/{filename}"
        
        # Convert text to speech using the correct method
        # According to documentation:
        # tts(text: str, speaker_idx: str = 'Linda', language_idx: str = 'th-th', 
        #     return_type: str = 'file', filename: Optional[str] = None)
        output_file = tts.tts(
            text=request.text,
            speaker_idx="Linda",
            language_idx="th-th",
            return_type="file",
            filename=output_path
        )
        
        # Debugging output
        print(f"TTS returned file path: {output_file}")
        print(f"Output path requested: {output_path}")
        print(f"File exists: {os.path.exists(output_path)}")
        
        # The method might return the actual file path, which could be different from our requested path
        # If the file exists at the returned path but not at our requested path, copy it
        if output_file and output_file != output_path and os.path.exists(output_file) and not os.path.exists(output_path):
            shutil.copyfile(output_file, output_path)
            print(f"Copied file from {output_file} to {output_path}")
        
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