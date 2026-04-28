from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def run_llama_rag():
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    #loading documents
    documents = SimpleDirectoryReader("data/raw").load_data()

    index = VectorStoreIndex.from_documents(documents)

    llm = Ollama(
    model="tinyllama",
    request_timeout=400.0 #increasing timeout since it is tinyllama and takes longer to respond - to avoid timeout errors
)

    query_engine = index.as_query_engine(llm=llm, response_mode="compact")

    print("LlamaIndex RAG ready! Ask questions.\n")

    while True:
        query = input("Ask: ")
        response = query_engine.query(query)
        print("\nAnswer:\n", response, "\n")