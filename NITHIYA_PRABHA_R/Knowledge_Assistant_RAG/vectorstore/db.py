from langchain_community.vectorstores import FAISS

def create_vector_store(docs, embeddings):
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore