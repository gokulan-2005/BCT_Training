import os
from dotenv import load_dotenv
from langchain_core.language_models.llms import LLM
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from groq import Groq

load_dotenv()

DB_URI = os.getenv("DB_URI")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def groq_call(prompt: str) -> str:
    """Call Groq LLM"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content

class GroqLLM(LLM):
    def _call(self, prompt, stop=None):
        return groq_call(prompt)
    @property
    def _llm_type(self):
        return "groq"

llm = GroqLLM()

db = SQLDatabase.from_uri(
    DB_URI,
    include_tables=["departments", "customers", "products", "orders"]
)

agent = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True,
    max_iterations=5,
    early_stopping_method="force",   
    handle_parsing_errors=True,     
)

def ask(question):
    print(f"\nQuestion: {question}")
    try:
        response = agent.invoke({"input": question})
        print("Answer:", response["output"])
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":

    ask("List all orders with customer name and product name")