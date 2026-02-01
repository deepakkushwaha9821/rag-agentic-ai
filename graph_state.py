from typing import TypedDict, List, Dict

class RAGState(TypedDict):
    question: str
    docs: List[Dict]
    answer: str
    confidence: float
