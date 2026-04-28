from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def nl_to_sql(question):
    prompt = f"""
Table: logs(timestamp, service, level, message, response_time)

Convert to SQL:
{question}

Return only SQL.
"""
    return llm.predict(prompt)

def insight_agent(question, result):
    prompt = f"""
User asked: {question}

Result: {result}

Explain what this means and identify issues or patterns.
"""
    return llm.predict(prompt)