from langgraph.graph import StateGraph, START, END
from graph_state import RAGState
from retrieve_node import retrieve_node
from generate_node import generate_node

graph = StateGraph(RAGState)

graph.add_node("retrieve", retrieve_node)
graph.add_node("generate", generate_node)

graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

rag_chatbot = graph.compile()
