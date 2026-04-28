
from langchain.prompts import PromptTemplate
from config import MODEL_NAME
from database.db import get_db

from langchain_groq import ChatGroq
from config import MODEL_NAME

llm = ChatGroq(
    model=MODEL_NAME,
    temperature=0
)

def get_relevant_tables(question):
    db = get_db()
    tables = db.get_usable_table_names()

    prompt = PromptTemplate(
    input_variables=["question", "tables"],
    template="""
You are a strict SQL assistant.

Available tables:
{tables}

User question:
{question}

Return ONLY the table names needed to answer the question.

Rules:
- Return ONLY table names
- No SQL queries
- No explanations
- No extra text
- Output must be comma-separated

Examples:
sales
customers
sales, customers
"""
)

    response = llm.invoke(prompt.format(
        question=question,
        tables=tables
    ))

    tables = response.content.strip()

    # Convert to list properly
    tables = [t.strip() for t in tables.split(",")]

    return tables