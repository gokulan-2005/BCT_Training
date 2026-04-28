import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Setup API Key
os.environ["GOOGLE_API_KEY"] = "YOUR_KEY_HERE"

# 2. LOAD & SPLIT
# Using your specific PDF name
file_path = "Drive_Guard_Versatile FOR PLAG.pdf"
loader = PyPDFLoader(file_path)
pages = loader.load()

# Technical docs usually need smaller chunks to keep details precise
text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
docs = text_splitter.split_documents(pages)

# 3. EMBEDDINGS (Using the exact name from your list)
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Create the vector database
vectorstore = Chroma.from_documents(
    documents=docs, 
    embedding=embeddings,
    persist_directory="./chroma_db" # This saves it so you don't re-embed every time
)

# 4. LLM SETUP (Using the Gemini 3 Flash from your list)
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)

# 5. THE MODERN RAG CHAIN
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, just say that you don't know. "
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# Create the chains
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(vectorstore.as_retriever(), question_answer_chain)

# 6. ASK!
response = rag_chain.invoke({"input": "What is DriveGuard and what are its main features?"})

print("\n--- FINAL ANSWER ---")
print(response["answer"])