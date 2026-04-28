from ingestion.loader import load_pdf
from ingestion.chunking import split_docs
from ingestion.embedding import get_embeddings
from vectorstore.db import create_vector_store
from langchain_community.llms import Ollama

def run_langchain_rag():
    #Load + process
    docs = load_pdf("data/raw/2.6 Ontological Representations and applications[1].pdf")
    chunks = split_docs(docs)
    embeddings = get_embeddings()
    db = create_vector_store(chunks, embeddings)

    llm = Ollama(model="tinyllama")#using tinyllama since it is a local model and laptop has limited resources

    print("LangChain ready! Ask questions.\n")

    while True:
        query = input("Ask: ")

        results = db.similarity_search(query, k=3)

        context = "\n".join([doc.page_content for doc in results])
    
        #promt for the model to answer
        prompt = f"""
        Answer the question based on the context below.

        Context:
        {context}

        Question:
        {query}
        """

        response = llm.invoke(prompt)

        print("\nAnswer:\n", response, "\n")
        