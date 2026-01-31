# import faiss, pickle, os
# from sentence_transformers import SentenceTransformer

# INDEX_PATH = "vectorstore/index.faiss"
# CHUNKS_PATH = "vectorstore/chunks.pkl"

# model = SentenceTransformer("BAAI/bge-base-en-v1.5")
# index = faiss.read_index(INDEX_PATH)

# with open(CHUNKS_PATH, "rb") as f:
#     chunks = pickle.load(f)

# def retrieve(query: str, top_k=5):
#     q_vec = model.encode([query])
#     scores, ids = index.search(q_vec, top_k)

#     results = []
#     for i, idx in enumerate(ids[0]):
#         results.append({
#             "text": chunks[idx].page_content,
#             "page": chunks[idx].metadata.get("page", 0),
#             "score": float(scores[0][i])
#         })

#     return results
import os
import pinecone
from sentence_transformers import SentenceTransformer

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENV"]
)

INDEX_NAME = "agentic-ai"
index = pinecone.Index(INDEX_NAME)

model = SentenceTransformer("BAAI/bge-base-en-v1.5")

def retrieve(query: str, top_k=5):
    q_vec = model.encode(query).tolist()

    res = index.query(
        vector=q_vec,
        top_k=top_k,
        include_metadata=True
    )

    results = []
    for match in res["matches"]:
        results.append({
            "text": match["metadata"]["text"],
            "page": match["metadata"]["page"],
            "score": 1 - match["score"]   
        })

    return results
