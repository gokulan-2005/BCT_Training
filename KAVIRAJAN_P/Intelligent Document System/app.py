from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import ollama

loader = PyPDFLoader("Sample01.pdf")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)


embeddings = OllamaEmbeddings(model="llama3")
db = FAISS.from_documents(docs, embeddings)

print("Document processed successfully!\n")

while True:
    query = input("Ask your question (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    results = db.similarity_search(query, k=3)

    context = "\n".join([doc.page_content for doc in results])

    prompt = f"""
    Answer the question based only on this context:
    {context}

    Question: {query}
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    print("\n Answer:")
    print(response['message']['content'])
    print("\n" + "-"*50 + "\n")