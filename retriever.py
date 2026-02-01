# import os
# from dotenv import load_dotenv
# from pinecone import Pinecone
# from sentence_transformers import SentenceTransformer

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ENV_PATH = os.path.join(BASE_DIR, ".env")

# load_dotenv(dotenv_path=ENV_PATH, override=True)

# print("DEBUG ENV:", os.getenv("PINECONE_API_KEY"))  # TEMP DEBUG

# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# if not PINECONE_API_KEY:
#     raise RuntimeError("PINECONE_API_KEY still not loaded")

# pc = Pinecone(api_key=PINECONE_API_KEY)
# index = pc.Index("agentic-ai")

# model = SentenceTransformer("BAAI/bge-base-en-v1.5")


# def retrieve(query: str, top_k: int = 5):
#     """
#     Retrieve top-k relevant chunks from Pinecone
#     """
#     q_vec = model.encode(query).tolist()

#     response = index.query(
#         vector=q_vec,
#         top_k=top_k,
#         include_metadata=True
#     )

#     results = []
#     for match in response["matches"]:
#         results.append({
#             "text": match["metadata"]["text"],
#             "page": match["metadata"].get("page", 0),
#             "score": 1 - match["score"]  # convert similarity to distance-like score
#         })

#     return results

import os
from dotenv import load_dotenv
load_dotenv()

import os
import faiss, pickle
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# ---------- EMBEDDING MODEL ----------
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# ---------- FAISS SETUP ----------
FAISS_INDEX_PATH = "vectorstore/index.faiss"
FAISS_CHUNKS_PATH = "vectorstore/chunks.pkl"

faiss_index = faiss.read_index(FAISS_INDEX_PATH)
with open(FAISS_CHUNKS_PATH, "rb") as f:
    faiss_chunks = pickle.load(f)

def retrieve_faiss(query: str, top_k=3):
    q_vec = model.encode([query])
    scores, ids = faiss_index.search(q_vec, top_k)

    results = []
    for i, idx in enumerate(ids[0]):
        results.append({
            "text": faiss_chunks[idx].page_content,
            "page": faiss_chunks[idx].metadata.get("page", 0),
            "score": float(scores[0][i])
        })
    return results

# ---------- PINECONE SETUP ----------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pinecone_index = pc.Index("agentic-ai")

def retrieve_pinecone(query: str, top_k=3):
    q_vec = model.encode(query).tolist()
    res = pinecone_index.query(
        vector=q_vec,
        top_k=top_k,
        include_metadata=True
    )

    results = []
    for m in res.matches:
        results.append({
            "text": m.metadata.get("text", ""),
            "page": m.metadata.get("page", 0),
            "score": 1 - m.score   # normalize
        })
    return results


def retrieve(query: str, top_k=3):
    try:
        results = retrieve_pinecone(query, top_k)

        # fallback conditions
        if not results:
            return retrieve_faiss(query, top_k)

        avg_score = sum(r["score"] for r in results) / len(results)
        if avg_score > 0.8:  # weak similarity
            return retrieve_faiss(query, top_k)

        return results

    except Exception:
        # Pinecone failure → FAISS fallback
        return retrieve_faiss(query, top_k)
