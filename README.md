# Agentic AI RAG Chatbot

A document-grounded Agentic AI chatbot built using:
- FastAPI
- Streamlit
- LangGraph
- SentenceTransformers
- FAISS / Pinecone
- GPT4All

## Features
- Strict RAG (no hallucinations)
- Confidence scoring
- Source chunk retrieval
- Local LLM inference

## Run locally

### Backend
```bash
python -m uvicorn api:app --reload --port 8000




#UI
streamlit run ui_streamlit.py


---

