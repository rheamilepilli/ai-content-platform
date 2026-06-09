from fastapi import FastAPI, UploadFile, File, Form
import shutil
import whisper
import os
import ollama

# Create uploads folder
os.makedirs("uploads", exist_ok=True)

app = FastAPI()

# Load Whisper model once when app starts
model = whisper.load_model("base")


@app.get("/")
def home():
    return {"message": "AI Content Platform Running"}


@app.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):
    # Save uploaded file
    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convert speech to text
    result = model.transcribe(file_location)
    transcript = result["text"]

    # Generate content using Qwen 2.5
    response = ollama.chat(
        model="qwen2.5",
        messages=[
            {
                "role": "user",
                "content": f"""
Transcript:

{transcript}

Based on this transcript, generate ALL of the following:

1. Instagram Caption
   - Under 50 words
   - Include emojis
   - Engaging and social-media friendly

2. LinkedIn Post
   - Professional tone
   - Well structured
   - Include a call to action

3. X (Twitter) Post
   - Under 280 characters
   - Attention-grabbing

4. YouTube Description
   - SEO-friendly
   - Include hashtags

User Style Request:
{prompt}

Clearly separate each section using these headings:

INSTAGRAM CAPTION:
LINKEDIN POST:
X POST:
YOUTUBE DESCRIPTION:
"""
            }
        ]
    )

    generated_content = response["message"]["content"]

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "prompt": prompt,
        "transcript": transcript,
        "generated_content": generated_content
    }