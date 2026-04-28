import argparse
import os
import time

from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec


# Hardcoded config (synced with current Pinecone index settings)
GEMINI_API_KEY = "AIzaSyDNu9cTOEkp4ib21RMVipUZtb3R3L20WMo"
PINECONE_API_KEY = "pcsk_3D1f7f_7TS9egzbsQkSfAupTJKXDct6Tme1Lt4deJDTssEQN32goHAM2x3BpCfpJ6drLNF"
PINECONE_INDEX = "rag-hf-384"
PINECONE_NAMESPACE = "default"
PINECONE_CLOUD = "aws"
PINECONE_REGION = "us-east-1"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHAT_MODEL = "gemini-3-flash-preview"

# LangChain's Pinecone integration expects this env var in some code paths.
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


def build_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def ensure_index(pc: Pinecone, index_name: str, cloud: str, region: str, dimension: int):
    existing = {x["name"] for x in pc.list_indexes()}
    if index_name not in existing:
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud=cloud, region=region),
        )
        while not pc.describe_index(index_name).status.get("ready"):
            time.sleep(1)


def ingest(pdf_dir: str):
    embeddings = build_embeddings()

    dim = len(embeddings.embed_query("dimension probe"))
    pc = Pinecone(api_key=PINECONE_API_KEY)
    ensure_index(pc, PINECONE_INDEX, PINECONE_CLOUD, PINECONE_REGION, dim)

    docs = PyPDFDirectoryLoader(pdf_dir).load()
    if not docs:
        print("No PDFs found.")
        return

    chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150).split_documents(docs)

    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=PINECONE_INDEX,
        namespace=PINECONE_NAMESPACE,
        pinecone_api_key=PINECONE_API_KEY,
    )

    print(f"Indexed {len(chunks)} chunks into index '{PINECONE_INDEX}' (namespace '{PINECONE_NAMESPACE}').")


def chat(top_k: int):
    embeddings = build_embeddings()

    vectorstore = PineconeVectorStore(
        index_name=PINECONE_INDEX,
        embedding=embeddings,
        namespace=PINECONE_NAMESPACE,
        pinecone_api_key=PINECONE_API_KEY,
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    llm = ChatGoogleGenerativeAI(model=CHAT_MODEL, google_api_key=GEMINI_API_KEY)
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

    print("\nRAG PDF Chat (type 'exit' to quit)\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue

        answer = qa.invoke({"query": question})["result"]
        print(f"\nAssistant: {answer}\n")


def main():
    parser = argparse.ArgumentParser(description="Simple RAG PDF chat with LangChain + Gemini + Pinecone")
    parser.add_argument("--top_k", type=int, default=4)
    sub = parser.add_subparsers(dest="cmd")

    p_ingest = sub.add_parser("ingest")
    p_ingest.add_argument("--pdf_dir", required=True)

    p_chat = sub.add_parser("chat")

    args = parser.parse_args()

    if args.cmd == "ingest":
        ingest(args.pdf_dir)
    elif args.cmd == "chat" or args.cmd is None:
        chat(args.top_k)


if __name__ == "__main__":
    main()
