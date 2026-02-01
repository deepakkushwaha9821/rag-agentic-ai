# # # from fastapi import FastAPI
# # # from pydantic import BaseModel
# # # from graph import rag_chatbot

# # # app = FastAPI(title="Agentic AI RAG Chatbot")

# # # class ChatRequest(BaseModel):
# # #     query: str

# # # @app.post("/chat")
# # # def chat(req: ChatRequest):
# # #     return rag_chatbot.invoke({"question": req.query})
# # from fastapi import FastAPI, HTTPException
# # from fastapi.middleware.cors import CORSMiddleware
# # from pydantic import BaseModel, Field
# # from typing import List, Dict, Optional
# # from graph import rag_chatbot
# # import uvicorn

# # # Initialize FastAPI app
# # app = FastAPI(
# #     title="RAG Chatbot API",
# #     description="Strictly grounded RAG chatbot for Agentic AI eBook",
# #     version="1.0.0"
# # )

# # # Add CORS middleware
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Request/Response models
# # class ChatRequest(BaseModel):
# #     question: str = Field(..., description="User's question", min_length=1)
    
# #     class Config:
# #         json_schema_extra = {
# #             "example": {
# #                 "question": "What is Agentic AI?"
# #             }
# #         }

# # class ChunkInfo(BaseModel):
# #     text: str
# #     page: int
# #     score: float

# # class ChatResponse(BaseModel):
# #     question: str
# #     answer: str
# #     confidence: float
# #     retrieved_chunks: List[ChunkInfo]
# #     citations: Optional[List[int]] = None
    
# #     class Config:
# #         json_schema_extra = {
# #             "example": {
# #                 "question": "What is Agentic AI?",
# #                 "answer": "According to Chunk 1, Agentic AI refers to...",
# #                 "confidence": 0.85,
# #                 "retrieved_chunks": [
# #                     {
# #                         "text": "Agentic AI is...",
# #                         "page": 5,
# #                         "score": 0.45
# #                     }
# #                 ],
# #                 "citations": [1]
# #             }
# #         }

# # # Health check endpoint
# # @app.get("/")
# # def read_root():
# #     return {
# #         "message": "RAG Chatbot API is running",
# #         "endpoints": {
# #             "chat": "/chat",
# #             "health": "/health",
# #             "docs": "/docs"
# #         }
# #     }

# # @app.get("/health")
# # def health_check():
# #     """Health check endpoint"""
# #     return {"status": "healthy"}

# # @app.post("/chat", response_model=ChatResponse)
# # def chat(request: ChatRequest):
# #     """
# #     Main chat endpoint - answers questions strictly based on the Agentic AI eBook
    
# #     Returns:
# #     - answer: Generated answer grounded in retrieved chunks
# #     - confidence: Confidence score (0.0 to 1.0)
# #     - retrieved_chunks: Source chunks used for generation
# #     - citations: Which chunks were cited in the answer
# #     """
# #     try:
# #         # Invoke the RAG graph
# #         result = rag_chatbot.invoke({"question": request.question})
        
# #         # Format chunks for response
# #         chunks = [
# #             ChunkInfo(
# #                 text=doc["text"],
# #                 page=doc["page"],
# #                 score=round(doc["score"], 4)
# #             )
# #             for doc in result.get("docs", [])
# #         ]
        
# #         answer = result.get("answer", "Not found in the provided document.")
# # confidence = result.get("confidence", 0.0)

# # return ChatResponse(
# #     question=request.question,
# #     answer=answer,
# #     confidence=confidence,
# #     retrieved_chunks=chunks,
# #     citations=result.get("citations", [])
# # )

        
# #     except Exception as e:
# #     print("🔥 CHAT ERROR:", repr(e))
# #     raise HTTPException(
# #         status_code=500,
# #         detail=str(e)
# #     )

# # if __name__ == "__main__":
# #     print("🚀 Starting RAG Chatbot API on http://localhost:8000")
# #     print("📖 Documentation available at http://localhost:8000/docs")
# #     uvicorn.run(app, host="0.0.0.0", port=8000)

# # from fastapi import FastAPI 
# # from pydantic import BaseModel
# # from graph import rag_chatbot

# # app = FastAPI(title="Agentic AI RAG Chatbot")

# # class ChatRequest(BaseModel):
# #     query: str

# # @app.post("/chat")
# # def chat(req: ChatRequest):
# #     return rag_chatbot.invoke({"question": req.query})

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, Field
# from typing import List, Dict, Optional
# from graph import rag_chatbot
# import uvicorn

# import json
# from datetime import datetime

# RESULT_FILE = "result.json"

# def save_result(data: dict):
#     record = {
#         "timestamp": datetime.utcnow().isoformat(),
#         **data
#     }

#     if os.path.exists(RESULT_FILE):
#         with open(RESULT_FILE, "r", encoding="utf-8") as f:
#             existing = json.load(f)
#     else:
#         existing = []

#     existing.append(record)

#     with open(RESULT_FILE, "w", encoding="utf-8") as f:
#         json.dump(existing, f, indent=2, ensure_ascii=False)


# # Initialize FastAPI app
# app = FastAPI(
#     title="RAG Chatbot API",
#     description="Strictly grounded RAG chatbot for Agentic AI eBook",
#     version="1.0.0"
# )

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Request/Response models
# class ChatRequest(BaseModel):
#     question: str = Field(..., description="User's question", min_length=1)

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "question": "What is Agentic AI?"
#             }
#         }


# class ChunkInfo(BaseModel):
#     text: str
#     page: int
#     score: float


# class ChatResponse(BaseModel):
#     question: str
#     answer: str
#     confidence: float
#     retrieved_chunks: List[ChunkInfo]
#     citations: Optional[List[int]] = None

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "question": "What is Agentic AI?",
#                 "answer": "According to Chunk 1, Agentic AI refers to...",
#                 "confidence": 0.85,
#                 "retrieved_chunks": [
#                     {
#                         "text": "Agentic AI is...",
#                         "page": 5,
#                         "score": 0.45
#                     }
#                 ],
#                 "citations": [1]
#             }
#         }


# # Health check endpoint
# @app.get("/")
# def read_root():
#     return {
#         "message": "RAG Chatbot API is running",
#         "endpoints": {
#             "chat": "/chat",
#             "health": "/health",
#             "docs": "/docs"
#         }
#     }


# @app.get("/health")
# def health_check():
#     """Health check endpoint"""
#     return {"status": "healthy"}


# @app.post("/chat", response_model=ChatResponse)
# def chat(request: ChatRequest):
    

  
#     try:
#         # Invoke the RAG graph
#         result = rag_chatbot.invoke({"question": request.question})

#         # Format chunks for response
#         chunks = [
#             ChunkInfo(
#                 text=doc["text"],
#                 page=doc["page"],
#                 score=round(doc["score"], 4)
#             )
#             for doc in result.get("docs", [])
#         ]
#         response_data = { 
#             "question": request.question,
#             "answer": answer,
#             "confidence": confidence,
#             "retrieved_chunks": [
#              {
#                 "page": c.page,
#                  "score": c.score,
#                   "text": c.text
#             }
#              for c in chunks
#     ]
# }

# save_result(response_data)
 
#         answer = result.get("answer", "Not found in the provided document.")
#         confidence = result.get("confidence", 0.0)

#         return ChatResponse(
#             question=request.question,
#             answer=answer,
#             confidence=confidence,
#             retrieved_chunks=chunks,
#             citations=result.get("citations", [])
#         )

#     except Exception as e:
#         print("🔥 CHAT ERROR:", repr(e))
#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )


# if __name__ == "__main__":
#     print("🚀 Starting RAG Chatbot API on http://localhost:8000")
#     print("📖 Documentation available at http://localhost:8000/docs")
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from graph import rag_chatbot
import uvicorn

import os
import json
from datetime import datetime

# ------------------ RESULT STORAGE ------------------
RESULT_FILE = "result.json"

def save_result(data: dict):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        **data
    }

    if os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    existing.append(record)

    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)


# ------------------ FASTAPI APP ------------------
app = FastAPI(
    title="RAG Chatbot API",
    description="Strictly grounded RAG chatbot for Agentic AI eBook",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------ MODELS ------------------
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)


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


# ------------------ HEALTH ------------------
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
    return {"status": "healthy"}


# ------------------ CHAT ------------------
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        # Invoke LangGraph
        result = rag_chatbot.invoke({"question": request.question})

        # Extract answer + confidence FIRST
        answer = result.get("answer", "Not found in the provided document.")
        confidence = result.get("confidence", 0.0)

        # Format retrieved chunks
        chunks = [
            ChunkInfo(
                text=doc["text"],
                page=doc["page"],
                score=round(doc["score"], 4)
            )
            for doc in result.get("docs", [])
        ]

        # Save EXACT result to result.json
        save_result({
            "question": request.question,
            "answer": answer,
            "confidence": confidence,
            "retrieved_chunks": [
                {
                    "page": c.page,
                    "score": c.score,
                    "text": c.text
                }
                for c in chunks
            ]
        })

        # Return API response (unchanged)
        return ChatResponse(
            question=request.question,
            answer=answer,
            confidence=confidence,
            retrieved_chunks=chunks,
            citations=result.get("citations", [])
        )

    except Exception as e:
        print("🔥 CHAT ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))


# ------------------ RUN ------------------
if __name__ == "__main__":
    print("🚀 Starting RAG Chatbot API on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
