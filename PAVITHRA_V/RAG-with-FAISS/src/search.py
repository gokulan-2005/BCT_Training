import os
from dotenv import load_dotenv
from src.vectorstore import FaissVectorStore
from langchain_groq import ChatGroq

load_dotenv()

class RAGSearch:
    def __init__(self,persist_dir: str = "faiss_store",embedding_model: str = "all-MiniLM-L6-v2",llm_model: str = "llama-3.1-8b-instant"):
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")

        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from data_loader import load_all_documents
            docs = load_all_documents("data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()

        groq_api_key = os.getenv("GROQ_API_KEY")
       
        self.llm = ChatGroq(groq_api_key=groq_api_key,model_name=llm_model)
        print(f"[INFO] Groq LLM initialized: {llm_model}")

    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        print(f"[INFO] Querying vector store for: '{query}'")
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [f"[Source {i+1}]: {r['metadata'].get('text', '')}" for i, r in enumerate(results) if r["metadata"] ]
        context = "\n\n".join(texts)
        
        if not context:
            return "No relevant documents found."

        prompt = f"""You are an AI assistant.
                    Answer the question using ONLY the provided context.
                    Be clear, concise, and direct.
                    Question:
                    {query}
                    Context:
                    {context}
                    Answer:
                """
        response = self.llm.invoke(prompt)
        return response.content.strip()

if __name__ == "__main__":
    rag_search = RAGSearch()
    query = "What is AI?"
    summary = rag_search.search_and_summarize(query, top_k=5)
    print("\n🔹 Final Answer:\n")
    print(summary)