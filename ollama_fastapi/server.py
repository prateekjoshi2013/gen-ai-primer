from fastapi import FastAPI
from pydantic import BaseModel
from ollama import Client

app = FastAPI()

client = Client(
    host="http://ollama:11434",
)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    response = client.chat(
        model="mistral:7b", messages=[{"role": "user", "content": request.message}]
    )
    return {"response": response.message.content}
