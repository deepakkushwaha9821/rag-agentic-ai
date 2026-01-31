from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss, pickle, os

loader = PyPDFLoader("data/Ebook-Agentic-AI.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=160
)
chunks = splitter.split_documents(docs)

model = SentenceTransformer("BAAI/bge-base-en-v1.5")
embeddings = model.encode([c.page_content for c in chunks], show_progress_bar=True)

dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

os.makedirs("vectorstore", exist_ok=True)
faiss.write_index(index, "vectorstore/index.faiss")

with open("vectorstore/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("✅ PDF ingested & vector store created")
