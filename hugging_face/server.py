from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from typing import List, Dict, Any
import os
from huggingface_hub import login

app = FastAPI(title="Hugging Face Image-Text-to-Text API")

# Authenticate with Hugging Face token from environment variable
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    try:
        login(token=hf_token, add_to_git_credential=False)
    except PermissionError:
        print("Warning: Could not save HF_TOKEN to cache directory due to permission restrictions.")
        print("Proceeding with token in memory only.")
else:
    print("Warning: HF_TOKEN environment variable not set. Authentication may be required.")

# Initialize the pipeline with 8-bit quantization for better memory efficiency
# Gemma-3-4B is a multimodal model that should fit in GPU memory
try:
    pipe = pipeline(
        "image-text-to-text",
        model="google/gemma-3-4b-it",
        device=0,  # Use GPU 0
        model_kwargs={"load_in_8bit": True},  # 8-bit quantization to reduce memory
    )
except Exception as e:
    print(f"Warning: Could not load model with GPU: {e}")
    print("Falling back to CPU inference...")
    try:
        pipe = pipeline("image-text-to-text", model="google/gemma-3-4b-it")
    except Exception as e2:
        print(f"Error loading model: {e2}")
        raise


class ImageTextRequest(BaseModel):
    image_url: str
    text: str


@app.get("/")
def read_root():
    return {"message": "Hugging Face Image-Text-to-Text API", "model": "google/gemma-3-4b-it"}


@app.post("/analyze")
def analyze_image_text(request: ImageTextRequest):
    """
    Analyze an image with a text prompt using the Gemma model
    """
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "url": request.image_url},
                {"type": "text", "text": request.text},
            ],
        },
    ]

    result = pipe(text=messages)
    return {"result": result}
