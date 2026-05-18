import streamlit as st
from rag.loader import load_pdf
from rag.retriever import index_documents
from rag.pipeline import generate_answer

st.set_page_config(page_title="RAG with LLaMA3", layout="wide")

st.title("📄 Chat with your PDF (LLaMA3 - Groq)")

# 🔹 Upload
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:

    # Only process ONCE
    if "processed" not in st.session_state:

        st.session_state.processed = False

        with st.spinner("📄 Reading PDF..."):
            text = load_pdf(uploaded_file)

        # 🚨 LIMIT TEXT (CRITICAL)
        text = text[:5000]

        with st.spinner("🧠 Indexing... (please wait)"):
            index_documents(text)

        st.session_state.processed = True
        st.success("✅ PDF processed!")

    # Ask question AFTER processing
    if st.session_state.processed:

        query = st.text_input("Ask your question:")

        if st.button("Ask"):
            if query.strip():
                with st.spinner("🤔 Thinking..."):
                    answer = generate_answer(query)

                st.write("### 💬 Answer")
                st.write(answer)
            else:
                st.warning("Enter a question")