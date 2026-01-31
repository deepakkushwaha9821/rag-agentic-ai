from graph import rag_chatbot

question = "What is Agentic AI?"

for i in range(1, 11):
    print(f"\n{'='*80}")
    print(f"[RUN {i}] QUESTION: {question}")
    print(f"{'='*80}")

    result = rag_chatbot.invoke({"question": question})

    print("ANSWER:")
    print(result["answer"])
    print("CONFIDENCE:", result["confidence"])
