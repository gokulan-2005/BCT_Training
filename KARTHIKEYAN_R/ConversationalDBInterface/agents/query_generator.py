from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from config import MODEL_NAME
from utils.helpers import clean_sql

llm = ChatGroq(
    model=MODEL_NAME,
    temperature=0
)

def generate_query(question, schema):
    prompt = PromptTemplate(
        input_variables=["question", "schema"],
        template="""
        You are a SQL expert.

        Schema:
        {schema}

        Question:
        {question}

        Write ONLY SQL query.
        """
    )

    response = llm.invoke(prompt.format(
        question=question,
        schema=schema
    ))

    return clean_sql(response.content)