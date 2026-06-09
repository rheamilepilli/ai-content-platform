from fastapi import FastAPI, UploadFile, File, Form
import shutil
import whisper
import os
import ollama

# Create uploads folder if it doesn't exist
os.makedirs("uploads", exist_ok=True)

app = FastAPI()

# Load Whisper model once when app starts
model = whisper.load_model("base")


@app.get("/")
def home():
    return {"message": "AI Content Platform Running"}


@app.post("/upload")
def upload_file(
    prompt: str = Form(...),
    file: UploadFile = File(...)
):
    # Save uploaded file
    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Transcribe video/audio
    result = model.transcribe(file_location)
    transcript = result["text"]

   
    response = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": f"""
Transcript:

{transcript}

User Request:

{prompt}

Follow the user's request exactly.
"""
            }
        ]
    )

    ai_response = response["message"]["content"].strip()

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "prompt": prompt,
        "transcript": transcript,
        "ai_response": ai_response
    }