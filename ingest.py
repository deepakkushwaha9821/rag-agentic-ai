# import os
# import pickle
# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from sentence_transformers import SentenceTransformer
# import faiss
# from pinecone import Pinecone

# # ------------------ CONFIG ------------------
# load_dotenv()

# PDF_PATH = "data/Ebook-Agentic-AI.pdf"
# INDEX_NAME = "agentic-ai"
# FAISS_DIR = "vectorstore"

# # ------------------ LOAD PDF ------------------
# loader = PyPDFLoader(PDF_PATH)
# docs = loader.load()

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=600,
#     chunk_overlap=160
# )
# chunks = splitter.split_documents(docs)

# # ------------------ EMBEDDINGS ------------------
# model = SentenceTransformer("BAAI/bge-base-en-v1.5")
# embeddings = model.encode(
#     [c.page_content for c in chunks],
#     show_progress_bar=True
# )

# dim = embeddings.shape[1]

# # ------------------ FAISS INGEST ------------------
# os.makedirs(FAISS_DIR, exist_ok=True)

# faiss_index = faiss.IndexFlatL2(dim)
# faiss_index.add(embeddings)

# faiss.write_index(faiss_index, f"{FAISS_DIR}/index.faiss")

# with open(f"{FAISS_DIR}/chunks.pkl", "wb") as f:
#     pickle.dump(chunks, f)

# print(f"✅ FAISS: stored {len(chunks)} chunks")

# # ------------------ PINECONE INGEST ------------------

# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
# pinecone_index = pc.Index(INDEX_NAME)

# vectors = []
# for i, chunk in enumerate(chunks):
#     vectors.append((
#         f"chunk-{i}",
#         embeddings[i].tolist(),
#         {
#             "text": chunk.page_content,
#             "page": chunk.metadata.get("page", 0)
#         }
#     ))

# for i in range(0, len(vectors), 100):
#     pinecone_index.upsert(vectors[i:i+100])

# print(f"✅ Pinecone: upserted {len(vectors)} chunks")

import os
import pickle
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
from pinecone import Pinecone

# ------------------ CONFIG ------------------
load_dotenv()

PDF_PATH = "data/Ebook-Agentic-AI.pdf"
INDEX_NAME = "agentic-ai"
FAISS_DIR = "vectorstore"

# ------------------ TEXT CLEANER (ADDED) ------------------
def clean_pdf_text(text: str) -> str:
    # Normalize broken bullets
    text = text.replace("�", "-")

    # Fix wrapped lines inside sentences / tables
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Restore bullet formatting
    text = re.sub(r"( - )", "\n- ", text)

    return text.strip()

# ------------------ LOAD PDF ------------------
loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

# =========================================================
# ✅ APPLY CLEANING (NOT REMOVING ANY LOGIC)
# =========================================================
for d in docs:
    d.page_content = clean_pdf_text(d.page_content)
# =========================================================

# ------------------ CHUNKING ------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=160
)
chunks = splitter.split_documents(docs)

# ------------------ EMBEDDINGS ------------------
model = SentenceTransformer("BAAI/bge-base-en-v1.5")
embeddings = model.encode(
    [c.page_content for c in chunks],
    show_progress_bar=True,
    normalize_embeddings=True
)

dim = embeddings.shape[1]

# ------------------ FAISS INGEST ------------------
os.makedirs(FAISS_DIR, exist_ok=True)

faiss_index = faiss.IndexFlatL2(dim)
faiss_index.add(embeddings)

faiss.write_index(faiss_index, f"{FAISS_DIR}/index.faiss")

with open(f"{FAISS_DIR}/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print(f"✅ FAISS: stored {len(chunks)} chunks")

# ------------------ PINECONE INGEST ------------------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pinecone_index = pc.Index(INDEX_NAME)

vectors = []
for i, chunk in enumerate(chunks):
    vectors.append((
        f"chunk-{i}",                      # unique ID
        embeddings[i].tolist(),            # 768-d vector
        {
            "text": chunk.page_content,    # cleaned text
            "page": chunk.metadata.get("page", 0)
        }
    ))

# Batch upsert (safe)
for i in range(0, len(vectors), 100):
    pinecone_index.upsert(vectors[i:i+100])

print(f"✅ Pinecone: upserted {len(vectors)} chunks")
