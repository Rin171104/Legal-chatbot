from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Backend API for RAG chatbot using Groq LLM",
    version="1.0.0"
)

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set")

client = Groq(api_key=groq_api_key)

# Request and Response Models
class ChatRequest(BaseModel):
    question: str = Field(..., description="User's question", min_length=1)

class Source(BaseModel):
    document: str = Field(..., description="Name of the source document")
    page: int = Field(..., description="Page number in the document")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="AI-generated answer")
    sources: List[Source] = Field(default_factory=list, description="List of source references")

# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "RAG Chatbot API is running",
        "version": "1.0.0"
    }

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process user question and return AI-generated answer with sources.
    """
    try:
        # Create chat completion using Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful, knowledgeable AI assistant. "
                        "Provide concise, accurate, and well-structured answers. "
                        "Use an academic but friendly tone. "
                        "When explaining complex topics, break them down into clear points."
                    )
                },
                {
                    "role": "user",
                    "content": request.question
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=1024,
            top_p=0.9,
            stream=False
        )
        
        # Extract answer from Groq response
        answer = chat_completion.choices[0].message.content
        
        # Generate demo sources (in a real RAG system, these would come from vector DB)
        sources = [
            Source(document="Demo Document", page=1),
            Source(document="Knowledge Base", page=5)
        ]
        
        return ChatResponse(
            answer=answer,
            sources=sources
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
