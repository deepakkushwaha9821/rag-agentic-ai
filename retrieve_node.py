from retriever import retrieve

def retrieve_node(state: dict):
    docs = retrieve(state["question"], top_k=5)
    return {
        "question": state["question"],
        "docs": docs
    }
