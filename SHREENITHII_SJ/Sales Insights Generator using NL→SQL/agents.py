from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def nl_to_sql_agent(question):
    prompt = f"""
Convert this natural language question into a SQL query for a table named sales with columns:
id, customer, product, region, amount

Question: {question}
Return only SQL.
"""
    return llm.predict(prompt)

def insight_agent(question, data):
    prompt = f"""
User asked: {question}

SQL result: {data}

Give a simple business insight from this data in 2-3 lines.
"""
    return llm.predict(prompt)