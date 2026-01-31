# import streamlit as st
# import requests

# st.title("📖 Agentic AI RAG Chatbot")

# query = st.text_input("Ask a question")

# if st.button("Ask") and query:
#     res = requests.post(
#         "http://localhost:8000/chat",
#         json={"query": query}
#     ).json()

#     st.subheader("Answer")
#     st.write(res["answer"])

#     st.subheader("Confidence")
#     st.write(res["confidence"])

#     st.subheader("Retrieved Context")
#     for d in res["docs"]:
#         st.markdown(f"**Page {d['page']}**")
#         st.caption(d["text"][:500])
import streamlit as st
import requests

st.title("📖 Agentic AI RAG Chatbot")

query = st.text_input("Ask a question")

if st.button("Ask") and query:
    try:
        res = requests.post(
            "http://localhost:8000/chat",
            json={"question": query},   # ✅ FIXED
            timeout=300
        )
        res.raise_for_status()
        data = res.json()

        st.subheader("Answer")
        st.write(data["answer"])

        st.subheader("Confidence")
        st.write(f"{data['confidence']:.0%}")

        st.subheader("Retrieved Context")
        for d in data["retrieved_chunks"]:   # ✅ FIXED
            st.markdown(f"**Page {d['page']}** (score {d['score']})")
            clean_text = (
                d["text"]
                .replace("�", "")
                .replace("###", "")
                .strip()
                 ) 
            st.caption(clean_text[:500])

    except requests.exceptions.ConnectionError:
        st.error("❌ Backend not running on port 8000")
    except Exception as e:
        st.error(f"Error: {e}")
