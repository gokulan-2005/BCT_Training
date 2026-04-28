from pandasai.llm.base import LLM
import requests
from app.config import GROQ_API_KEY, GROQ_BASE_URL, MODEL


class GroqLLM(LLM):

    @property
    def type(self):
        return "groq"

    def call(self, prompt, context=None) -> str:

        if not isinstance(prompt, str):
            prompt = str(prompt)

        prompt = f"""
You are a Python data analyst working with Pandas and SQL.

STRICT RULES:
- Generate ONLY executable Python code
- DO NOT explain anything
- DO NOT return markdown or text
- DO NOT wrap in backticks
- DO NOT output groupby unless required

IMPORTANT OUTPUT RULES:
- You MUST use execute_sql_query() for data fetching
- Final output MUST be stored in variable: result
- result MUST be a PANDAS DATAFRAME (NOT dict, NOT string)

CORRECT FORMAT:
result = execute_sql_query("SELECT ...")

OR:
df = execute_sql_query("SELECT ...")
result = df.head(10)

OR summary:
df = execute_sql_query("SELECT ...")
result = df.describe(include='all')

USER QUESTION:
{prompt}
"""

        url = f"{GROQ_BASE_URL}/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,  
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Groq API Error: {response.text}")

        return response.json()["choices"][0]["message"]["content"]