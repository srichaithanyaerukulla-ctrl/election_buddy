import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.cloud import firestore
from fastapi.middleware.cors import CORSMiddleware
from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='frontend')

@app.route('/')
def home():
    return send_from_directory('frontend', 'index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
# Initialize FastAPI
app = FastAPI(title="Election Buddy Backend")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
PROJECT_ID = "project-c4cd6ab1-66ee-44df-88b"
LOCATION = "us-central1"  # Or your preferred location
vertexai.init(project=PROJECT_ID, location=LOCATION)
db = firestore.Client(project=PROJECT_ID)

# AI Model Initialization
model = GenerativeModel("gemini-1.5-flash") # Using 1.5 flash as it's the current standard

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []

class LogRequest(BaseModel):
    user_query: str
    bot_response: str
    timestamp: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Load the master prompt
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "master_prompt.txt")
        with open(prompt_path, "r") as f:
            system_instructions = f.read()

        # Combine system instructions with user message
        full_prompt = f"{system_instructions}\n\nUser: {request.message}"
        
        response = model.generate_content(full_prompt)
        
        return {"response": response.text}
    except Exception as e:
        print(f"Error in /chat: {str(e)}")
        # Fallback for demonstration if API fails or isn't configured
        return {"response": "I'm sorry, I'm having trouble connecting to my brain right now. Please try again or call the helpline at 1950."}

@app.get("/crowd")
async def get_crowd_status():
    """Simulated crowd data for various booths"""
    try:
        # In a real scenario, this would query Firestore for real-time crowd reports
        # For now, we return simulated data
        booths = [
            {"id": "B001", "name": "Primary School East", "status": "Low", "wait_time": "10 mins"},
            {"id": "B002", "name": "Community Center North", "status": "Medium", "wait_time": "30 mins"},
            {"id": "B003", "name": "Govt High School South", "status": "High", "wait_time": "1 hour+"}
        ]
        return {"booths": booths}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/log")
async def log_query(request: LogRequest):
    try:
        # Store query log in Firestore
        doc_ref = db.collection("logs").document()
        doc_ref.set({
            "query": request.user_query,
            "response": request.bot_response,
            "timestamp": request.timestamp
        })
        return {"status": "success"}
    except Exception as e:
        print(f"Logging error: {str(e)}")
        return {"status": "error", "message": "Failed to log"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
