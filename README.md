Agentic AI RAG Chatbot
A document-grounded Retrieval-Augmented Generation (RAG) chatbot developed in Python. This system answers queries exclusively using data from the Agentic AI eBook. It is engineered to prioritize accuracy, minimize hallucination, and provide transparent confidence metrics via both a REST API and a graphical user interface.

Technology Stack
FastAPI: Backend API framework.

Streamlit: Interactive chat interface.

LangGraph: Orchestration framework for RAG workflows.

SentenceTransformers: Text embedding models (BAAI/bge-base-en-v1.5).

FAISS / Pinecone: Vector database solutions (supports both local and cloud deployments).

GPT4All: Local Large Language Model (LLM) inference.

Key Features
Domain-Specific Retrieval: Answers are strictly derived from the source PDF to ensure data integrity.

Advanced Ingestion Pipeline: Includes normalization for text, tables, and lists.

Semantic Search: Utilizes high-dimensional vector search for accurate context retrieval.

Confidence Scoring: Provides similarity metrics to gauge the reliability of the retrieved information.

Context Transparency: Returns the specific document chunks used to generate the answer.

Local Inference: Runs entirely on local infrastructure without reliance on external AI coding platforms.

System Architecture
High-Level Workflow
Plaintext
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
Ingestion Pipeline
Plaintext
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
Retrieval-Augmented Generation (RAG) Logic
The pipeline uses LangGraph to orchestrate the flow between two primary nodes:

Retrieve Node:

Encodes the user query into a vector.

Queries the FAISS or Pinecone index to fetch the top-k most relevant text chunks.

Generate Node:

Constructs a prompt using strictly the retrieved chunks.

Generates an answer only if the information is explicitly present in the source text.

If the information is missing, the system returns a standardized fallback response:

"Not found in the provided document."

Project Structure
Plaintext
rag-agentic-ai/
│
├── api.py                  # FastAPI backend application
├── ui_streamlit.py         # Streamlit frontend interface
├── ingest.py               # Data ingestion script (PDF → Vector Store)
├── graph.py                # LangGraph pipeline definition
├── graph_state.py          # State management for RAG workflow
├── retrieve_node.py        # Logic for document retrieval
├── generate_node.py        # Logic for answer generation and scoring
├── retriever.py            # Interface for FAISS/Pinecone interactions
├── llm.py                  # Configuration for GPT4All local LLM
│
├── data/
│   └── Ebook-Agentic-AI.pdf
│
├── vectorstore/            # Storage for FAISS index and chunks
├── models/                 # Directory for local LLM binaries
│
├── requirements.txt
├── README.md
└── .env
Installation and Execution
1. Install Dependencies
Ensure you have a compatible Python environment, then install the required packages:

Bash
pip install -r requirements.txt
2. Ingest Data
Run the ingestion script to process the source document. This process includes loading the PDF, cleaning the text (preserving table structures), chunking the content, generating embeddings, and storing vectors in FAISS or Pinecone.

Bash
python ingest.py
3. Start the Backend API
Launch the FastAPI server using Uvicorn.

Bash
python -m uvicorn api:app --reload --port 8000
API Documentation: Available at http://localhost:8000/docs

4. Launch the User Interface (Optional)
Start the Streamlit application to interact with the chatbot via a web interface.

Bash
streamlit run ui_streamlit.py
