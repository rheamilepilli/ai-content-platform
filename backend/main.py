from fastapi import FastAPI, UploadFile, File, Form
import shutil
import whisper
import os
import ollama

os.makedirs("uploads", exist_ok=True)

app = FastAPI()

model = whisper.load_model("base")

@app.get("/")
def home():
    return {"message": "AI Content Platform Running"}

@app.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):

    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = model.transcribe(file_location)

    transcript = result["text"]

    response = ollama.chat(
        model="qwen2.5",
        messages=[
            {
                "role": "user",
                "content": f"""
                Transcript:

                {transcript}

                User Request:

                {prompt}
                """
            }
        ]
    )

    ai_output = response["message"]["content"]

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "transcript": transcript,
        "ai_response": ai_output
    }