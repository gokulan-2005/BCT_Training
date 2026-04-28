import os
from dotenv import load_dotenv

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

load_dotenv()

def load_documents(path):
    docs = []
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(path, file))
            docs.extend(loader.load())
    return docs

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)

def create_vectorstore(docs):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(docs, embeddings)

def build_chain(vectorstore):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return chain

def main():
    print("\nEnterprise Knowledge Assistant is starting...\n")

    documents_path = "documents"
    documents = load_documents(documents_path)

    if not documents:
        print("No documents found. Add PDFs inside the 'documents' folder.")
        return

    docs = split_documents(documents)
    vectorstore = create_vectorstore(docs)
    chain = build_chain(vectorstore)

    print("System ready. Ask anything about your documents (type 'exit' to quit)\n")

    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit"]:
            print("\nExiting.\n")
            break

        try:
            result = chain({"question": query})
            answer = result.get("answer", "")

            print("\nAssistant:")
            print(answer)
            print("\n" + "-" * 60 + "\n")

        except Exception as e:
            print("\nError:", str(e), "\n")

if __name__ == "__main__":
    main()