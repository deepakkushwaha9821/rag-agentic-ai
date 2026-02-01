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
You are a document-grounded AI assistant.

You MUST follow ALL rules below. There are NO exceptions.


STRICT CONTENT RULES

- Answer ONLY using factual, descriptive content explicitly present in the provided PDF.
- Read ALL provided content carefully, including:
  - Paragraph text
  - Tables text
  - Headings and subheadings
  - Bullet points
  - Any text appearing under or within sections
- Do NOT use opinions, quotes, assumptions, or future-looking statements.
- Do NOT explain beyond what is explicitly written.
- Do NOT summarize, generalize, infer, or add interpretation.
- Do NOT introduce comparisons unless they are explicitly written in the document.
- Do NOT use outside knowledge.

- You MAY combine information from multiple sections ONLY if they describe the SAME concept
  using explicit wording from the document.


QUESTION HANDLING RULES

- If the question starts with "What is", return a definition-style answer ONLY if an explicit
  definition exists in the document.
- If the question asks to list items, return ONLY the items explicitly listed in the document.
- If the question asks about a concept that is not clearly and explicitly stated, return exactly:
  "Not found in the provided document."


  


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
