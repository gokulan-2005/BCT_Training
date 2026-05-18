# rag/retriever.py

import faiss
import numpy as np
from rag.embedder import get_embeddings

# 🔹 Global storage
index = None
documents = []


def index_documents(text):
    global index, documents

    # 🔹 Reset everything
    documents = []

    # 🔹 Limit text
    text = text[:5000]

    # 🔹 Chunking
    chunks = [text[i:i+400] for i in range(0, len(text), 400)]

    if not chunks:
        return

    documents = chunks

    # 🔹 Generate embeddings
    embeddings = get_embeddings(chunks)

    embeddings = np.array(embeddings).astype("float32")

    # 🔹 Create FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)

    index.add(embeddings)


def retrieve(query, k=3):
    global index, documents

    if index is None:
        return []

    query_embedding = get_embeddings([query])[0]
    query_embedding = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_embedding, k)

    results = []
    for i in indices[0]:
        if i < len(documents):
            results.append(documents[i])

    return results