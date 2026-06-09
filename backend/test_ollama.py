import ollama

response = ollama.chat(
    model="qwen2.5",
    messages=[
        {
            "role": "user",
            "content": "Write an Instagram caption about AI helping content creators."
        }
    ]
)

print(response["message"]["content"])