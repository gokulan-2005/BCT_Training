import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from crewai import LLM, Agent, Task, Crew
from crewai.tools import tool  # Changed from crewai_tools import tool

load_dotenv()

# Initialize LLMs
cohere_llm = ChatCohere(
    model="command",
    temperature=0.3,
    cohere_api_key=os.getenv("COHERE_API_KEY")
)

crew_llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.1
)

# Global variable to store vector store
vector_store = None


# PDF Processing Functions
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    global vector_store
    embeddings = CohereEmbeddings(
        model="embed-english-v3.0",
        cohere_api_key=os.getenv("COHERE_API_KEY")
    )
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store


# Custom RAG Tool for CrewAI
@tool("PDF Search Tool")
def pdf_search_tool(query: str) -> str:
    """Search through uploaded PDF documents for relevant information."""
    global vector_store

    if vector_store is None:
        try:
            embeddings = CohereEmbeddings(
                model="embed-english-v3.0",
                cohere_api_key=os.getenv("COHERE_API_KEY")
            )
            vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        except:
            return "No PDF documents have been uploaded and processed yet."

    try:
        docs = vector_store.similarity_search(query, k=5)
        context = "\n\n".join([doc.page_content for doc in docs])
        return f"Retrieved context from PDFs:\n{context}"
    except Exception as e:
        return f"Error searching PDFs: {str(e)}"


# CrewAI Agents
def create_agents():
    research_agent = Agent(
        role="PDF Research Specialist",
        goal="Extract and analyze relevant information from uploaded PDF documents based on user queries: {query}",
        backstory="You are an expert at finding and analyzing information from PDF documents. You can search through document contents and provide detailed, factual responses.",
        verbose=True,
        llm=crew_llm,
        tools=[pdf_search_tool]
    )

    writer_agent = Agent(
        role="Research Summarizer and Writer",
        goal="Create comprehensive summaries and detailed responses based on PDF research findings",
        backstory="You are skilled at synthesizing information from multiple sources and creating clear, well-structured responses that directly answer user questions.",
        verbose=True,
        llm=crew_llm
    )

    return research_agent, writer_agent


# CrewAI Tasks
def create_tasks(query, research_agent, writer_agent):
    research_task = Task(
        description=f"""
        Search through the uploaded PDF documents for information related to: {query}

        Your task is to:
        1. Use the PDF search tool to find relevant information
        2. Extract key facts, details, and context
        3. Identify the most relevant sections that answer the user's question
        4. Compile comprehensive findings from the documents
        """,
        expected_output="Detailed research findings with relevant quotes and information from the PDF documents",
        agent=research_agent,
    )

    writing_task = Task(
        description=f"""
        Based on the research findings from the PDF documents, create a comprehensive response to: {query}

        Your response should:
        1. Directly address the user's question
        2. Include specific details and facts from the documents
        3. Be well-structured and easy to understand
        4. Cite relevant information where appropriate
        5. If the answer isn't in the documents, clearly state that
        """,
        expected_output="A detailed, well-structured response that answers the user's question based on the PDF content",
        agent=writer_agent,
        context=[research_task]
    )

    return research_task, writing_task


# Agentic RAG Processing
def process_agentic_query(user_question):
    try:
        research_agent, writer_agent = create_agents()
        research_task, writing_task = create_tasks(user_question, research_agent, writer_agent)

        crew = Crew(
            agents=[research_agent, writer_agent],
            tasks=[research_task, writing_task],
            verbose=True,
        )

        result = crew.kickoff(inputs={"query": user_question})
        return result
    except Exception as e:
        st.error(f"Error in agentic processing: {str(e)}")
        return "I encountered an error while processing your request. Please try again."


# Load vector store function
def load_existing_vector_store():
    global vector_store

    if vector_store is None:
        try:
            embeddings = CohereEmbeddings(
                model="embed-english-v3.0",
                cohere_api_key=os.getenv("COHERE_API_KEY")
            )
            vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
            return True
        except:
            return False
    return True


# Streamlit UI
def main():
    st.set_page_config(page_title="Agentic RAG Chat with PDFs", layout="wide")
    st.header("🤖 Agentic RAG: AI Research Assistant for PDF Documents", divider='rainbow')

    # Sidebar for PDF upload
    with st.sidebar:
        st.title("📁 Document Management")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files",
            accept_multiple_files=True,
            help="Upload one or more PDF files to analyze"
        )

        if st.button("🔄 Process Documents", type="primary"):
            if pdf_docs:
                with st.spinner("Processing documents..."):
                    try:
                        raw_text = get_pdf_text(pdf_docs)
                        text_chunks = get_text_chunks(raw_text)
                        get_vector_store(text_chunks)
                        st.success("✅ Documents processed successfully!")
                        st.info(f"Processed {len(pdf_docs)} document(s)")
                    except Exception as e:
                        st.error(f"Error processing documents: {str(e)}")
            else:
                st.warning("Please upload PDF files first!")

        st.markdown("---")
        st.markdown("### 📋 How to Use:")
        st.markdown("""
        1. **Upload PDFs**: Select one or more PDF files
        2. **Process**: Click 'Process Documents' 
        3. **Ask Questions**: Type your question below
        4. **Get AI Research**: Our agents will analyze and respond
        """)

    # Main chat interface
    st.markdown("### 💬 Ask Questions About Your Documents")

    user_question = st.text_input(
        "What would you like to know about your documents?",
        placeholder="e.g., What are the main findings in the research paper?",
        help="Ask specific questions about the content in your uploaded PDFs"
    )

    col1, col2 = st.columns([1, 4])

    with col1:
        ask_button = st.button("🔍 Ask AI Agents", type="primary")

    with col2:
        if st.button("🗑️ Clear Response"):
            st.rerun()

    # Process query with agentic system
    if ask_button and user_question:
        if not load_existing_vector_store():
            st.error("❌ Please upload and process documents first!")
            return

        with st.spinner("🤖 AI agents are researching your question..."):
            response = process_agentic_query(user_question)

            st.markdown("### 📝 AI Research Response:")
            st.markdown("---")

            # Display the response in a nice format
            if hasattr(response, 'raw'):
                st.write(response.raw)
            else:
                st.write(str(response))

    elif user_question and not ask_button:
        st.info("👆 Click 'Ask AI Agents' to get your answer!")

    # Display some example questions if no PDFs processed yet
    global vector_store
    if vector_store is None and not load_existing_vector_store():
        st.markdown("### 💡 Example Questions You Can Ask:")
        st.markdown("""
        - "What are the main conclusions of this research?"
        - "Summarize the methodology used in the study"
        - "What are the key findings about [specific topic]?"
        - "Can you explain the results in simple terms?"
        - "What recommendations does the document make?"
        """)


if __name__ == "__main__":
    main()
