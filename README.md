# Agentic AI RAG Chatbot

A **document-grounded Retrieval-Augmented Generation (RAG) chatbot** developed in Python. This system answers queries **exclusively** using data from the *Agentic AI eBook*. It is engineered to prioritize accuracy, minimize hallucination, and provide **transparent confidence metrics** via both a REST API and an optional graphical user interface.

---

## Technology Stack

* **FastAPI** — Backend API framework
* **Streamlit** — Interactive chat interface
* **LangGraph** — Orchestration framework for RAG workflows
* **SentenceTransformers** — Text embedding models (`BAAI/bge-base-en-v1.5`)
* **FAISS / Pinecone** — Vector database solutions (local and cloud)
* **qwen2.5-3b-instruct-q4_k_m.gguf** — Local Large Language Model (LLM) inference

---

## Key Features

* **Domain-Specific Retrieval**
  Answers are strictly derived from the source PDF to ensure data integrity.

* **Advanced Ingestion Pipeline**
  Normalization and cleaning for text, tables, and lists.

* **Semantic Search**
  High-dimensional vector similarity search for accurate context retrieval.

* **Confidence Scoring**
  Similarity-based metrics to estimate the reliability of responses.

* **Context Transparency**
  Returns the exact document chunks used to generate each answer.

* **Local Inference**
  Fully local execution with no dependency on external AI coding platforms.

---

## System Architecture

### High-Level Workflow

```plaintext
User Question
      |
      v
Streamlit UI (Optional)
      |
      v
FastAPI Endpoint (/chat)
      |
      v
LangGraph RAG Pipeline
      |
      +----------------------+
      |                      |
      v                      v
Retrieve Node          Generate Node
(Vector DB)               (LLM)
      |                      |
      v                      v
Relevant Chunks        Grounded Answer
      |                      |
      +----------+-----------+
                 |
                 v
           Final Response
 (Answer + Confidence + Context)
```

---

### Ingestion Pipeline

```plaintext
PDF Source (Agentic AI eBook)
             |
             v
        PyPDFLoader
             |
             v
       Text Cleaning
(bullets, tables, line breaks)
             |
             v
         Chunking
(RecursiveCharacterTextSplitter)
             |
             v
   Embeddings (768-dim)
  (SentenceTransformers)
             |
             v
       Vector Store
    ├─ FAISS (Local)
    └─ Pinecone (Cloud)
```

---

## Retrieval-Augmented Generation (RAG) Logic

The pipeline uses **LangGraph** to orchestrate the interaction between two primary nodes:

### Retrieve Node

* Encodes the user query into a vector
* Queries FAISS or Pinecone to retrieve the **top-k most relevant chunks**

### Generate Node

* Constructs a prompt using **only** the retrieved chunks
* Generates an answer **only if** the information exists in the source text
* If no relevant information is found, the system returns the standardized fallback:

```text
Not found in the provided document.
```

---

## Project Structure

```plaintext
rag-agentic-ai/
│
├── api.py                  # FastAPI backend application
├── ui_streamlit.py         # Streamlit frontend interface
├── ingest.py               # Data ingestion (PDF → Vector Store)
├── graph.py                # LangGraph pipeline definition
├── graph_state.py          # RAG workflow state management
├── retrieve_node.py        # Document retrieval logic
├── generate_node.py        # Answer generation and confidence scoring
├── retriever.py            # FAISS / Pinecone abstraction layer
├── llm.py                  # qwen2.5-3b-instruct-q4_k_m.gguf local LLM configuration
│
├── data/
│   └── Ebook-Agentic-AI.pdf
│
├── vectorstore/            # FAISS index and stored chunks
├── models/                 # Local LLM binaries
│
├── requirements.txt
├── README.md
└── .env
```

---

## Installation and Execution

### 1. Install Dependencies

Ensure you have a compatible Python environment, then install all required packages:

```bash
pip install -r requirements.txt
```

---

### 2. Ingest Data

Run the ingestion script to process the source document. This step includes:

* Loading the PDF
* Cleaning and normalizing text (including tables)
* Chunking content
* Generating embeddings
* Persisting vectors in FAISS or Pinecone

```bash
python ingest.py
```

---

### 3. Start the Backend API

Launch the FastAPI server using Uvicorn:

```bash
python -m uvicorn api:app --reload --port 8000
```

**API Documentation:**
Available at `http://localhost:8000/docs`

---

### 4. Launch the User Interface (Optional)

Start the Streamlit application to interact with the chatbot through a web UI:

```bash
streamlit run ui_streamlit.py
```

---

## Notes

* The system is intentionally restrictive by design to prevent hallucination.
* All responses are grounded in the provided document and include traceable context.
* Suitable for research, internal knowledge bases, and compliance-sensitive environments.
