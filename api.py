# from fastapi import FastAPI
# from pydantic import BaseModel
# from graph import rag_chatbot

# app = FastAPI(title="Agentic AI RAG Chatbot")

# class ChatRequest(BaseModel):
#     query: str

# @app.post("/chat")
# def chat(req: ChatRequest):
#     return rag_chatbot.invoke({"question": req.query})
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from graph import rag_chatbot
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Strictly grounded RAG chatbot for Agentic AI eBook",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    question: str = Field(..., description="User's question", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is Agentic AI?"
            }
        }

class ChunkInfo(BaseModel):
    text: str
    page: int
    score: float

class ChatResponse(BaseModel):
    question: str
    answer: str
    confidence: float
    retrieved_chunks: List[ChunkInfo]
    citations: Optional[List[int]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is Agentic AI?",
                "answer": "According to Chunk 1, Agentic AI refers to...",
                "confidence": 0.85,
                "retrieved_chunks": [
                    {
                        "text": "Agentic AI is...",
                        "page": 5,
                        "score": 0.45
                    }
                ],
                "citations": [1]
            }
        }

# Health check endpoint
@app.get("/")
def read_root():
    return {
        "message": "RAG Chatbot API is running",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main chat endpoint - answers questions strictly based on the Agentic AI eBook
    
    Returns:
    - answer: Generated answer grounded in retrieved chunks
    - confidence: Confidence score (0.0 to 1.0)
    - retrieved_chunks: Source chunks used for generation
    - citations: Which chunks were cited in the answer
    """
    try:
        # Invoke the RAG graph
        result = rag_chatbot.invoke({"question": request.question})
        
        # Format chunks for response
        chunks = [
            ChunkInfo(
                text=doc["text"],
                page=doc["page"],
                score=round(doc["score"], 4)
            )
            for doc in result.get("docs", [])
        ]
        
        return ChatResponse(
            question=request.question,
            answer=result["answer"],
            confidence=result["confidence"],
            retrieved_chunks=chunks,
            citations=result.get("citations", [])
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing request: {str(e)}"
        )

if __name__ == "__main__":
    print("🚀 Starting RAG Chatbot API on http://localhost:8000")
    print("📖 Documentation available at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
