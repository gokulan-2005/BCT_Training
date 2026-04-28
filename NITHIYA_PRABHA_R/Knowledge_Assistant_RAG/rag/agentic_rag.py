from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from tools.retriever import retrieve
from tools.summarizer import summarize
from tools.analyzer import analyze


def run_agentic_rag():

    Settings.embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    documents = SimpleDirectoryReader("data/raw").load_data()
    index = VectorStoreIndex.from_documents(documents)

    llm = Ollama(model="tinyllama", request_timeout=300.0)

    query_engine = index.as_query_engine(
        llm=llm,
        response_mode="tree_summarize"   
    )

    print(" Full Agentic RAG Ready!\n")

    memory = []

    while True:
        query = input("Ask: ")

        print("\n[Thinking...]")

        query_lower = query.lower()

        if any(word in query_lower for word in ["summarize", "summary"]):
            action = "summarize"

        elif any(word in query_lower for word in ["explain", "why", "analyze", "examples"]):
            action = "analyze"

        elif any(word in query_lower for word in ["compare", "difference"]):
            action = "analyze"

        else:
            action = "retrieve"

        print(f"[Chosen Tool: {action}]")

        if action == "summarize":
            result = summarize(query_engine)

        elif action == "analyze":
            result = analyze(query_engine, query)

        else:
            result = retrieve(query_engine, query)

        memory.append((query, str(result)))

        print("\nAnswer:\n", result)

        print("\n--- Conversation Memory ---")
        for q, r in memory[-2:]:
            print(f"Q: {q}")
            print(f"A: {r}\n")