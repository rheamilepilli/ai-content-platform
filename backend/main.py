from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import whisper
import os
import ollama

# Create uploads folder
os.makedirs("uploads", exist_ok=True)

app = FastAPI()

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Whisper model once
model = whisper.load_model("base")


@app.get("/")
def home():
    return {"message": "AI Content Platform Running"}


@app.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    content_type: str = Form(...),
    style: str = Form(...),
    custom_prompt: str = Form("")
):

    # Save uploaded file
    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Transcribe audio/video
    result = model.transcribe(file_location)
    transcript = result["text"]

    # Check transcript length
    if len(transcript.split()) < 20:
        return {
            "error": "Transcript is too short. Please upload a longer video with at least 20 words.",
            "transcript": transcript
        }

    # Decide content type
    if content_type == "Instagram":
        content_instruction = """
Generate 3 Instagram captions.
Keep them short, engaging, and platform-friendly.
Use emojis where appropriate.
"""

    elif content_type == "LinkedIn":
        content_instruction = """
Generate a professional LinkedIn post.
Use a clear structure and include a call to action.
"""

    elif content_type == "Twitter":
        content_instruction = """
Generate 3 X/Twitter posts.
Each must be under 280 characters.
"""

    elif content_type == "YouTube":
        content_instruction = """
Generate a YouTube description.
Make it SEO-friendly and include hashtags.
"""

    else:
        content_instruction = """
Generate:

1. Three Instagram captions
2. One LinkedIn post
3. Three X/Twitter posts
4. One YouTube description
"""

    prompt_text = f"""
Transcript:

{transcript}

IMPORTANT RULES:

1. Only use information from the transcript.
2. Do not invent facts, events, products, people, or stories.
3. Stay faithful to the original content.
4. Follow the requested style.
5. If information is limited, say so instead of making things up.

STYLE:
{style}

ADDITIONAL USER REQUEST:
{custom_prompt}

TASK:
{content_instruction}
"""

    response = ollama.chat(
        model="qwen2.5",
        messages=[
            {
                "role": "user",
                "content": prompt_text
            }
        ]
    )

    generated_content = response["message"]["content"]

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "content_type": content_type,
        "style": style,
        "custom_prompt": custom_prompt,
        "transcript": transcript,
        "generated_content": generated_content
    }