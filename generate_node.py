from llm import generate
import random

FORBIDDEN_PHRASES = [
    "according to",
    "chunk",
    "therefore",
    "in summary",
    "this means",
]

def generate_node(state: dict):
    docs = state.get("docs", [])
    random.shuffle(docs)
    question = state.get("question", "")

    # ❌ No retrieved docs
    if not docs:
        return {
            "answer": "Not found in the provided document.",
            "confidence": 0.0,
            "docs": []
        }

    context = "\n\n".join(doc["text"] for doc in docs)

    prompt = f"""
You are a document-grounded assistant.

Rules:
- Read the PDF carefully.
- Return ONLY information present in the document.
- Do NOT explain or summarize.
- Do NOT add external knowledge.

Context:
{context}

Question:
{question}

Answer:
"""

    answer = generate(prompt).strip()
    lower = answer.lower()

    # 🔒 Strict answer enforcement
    if (
        not answer
        or "not found in the provided document" in lower
        or any(p in lower for p in FORBIDDEN_PHRASES)
        or len(answer.split()) > 200
    ):
        return {
            "answer": "Not found in the provided document.",
            "confidence": 0.0,
            "docs": docs
        }

    # ✅ REAL CONFIDENCE CALCULATION (0.0 – 1.0)
    scores = [doc["score"] for doc in docs if "score" in doc]

    if scores:
        best_score = min(scores)          # lower FAISS score = better
        confidence = 1 - best_score
    else:
        confidence = 0.0

    # Clamp to valid range
    confidence = max(0.0, min(confidence, 1.0))
    confidence = round(confidence, 2)

    # Penalize weak answers
    if len(answer.split()) < 15:
        confidence *= 0.6

    return {
        "answer": answer,
        "confidence": confidence,
        "docs": docs
    }
