def analyze(query_engine, query):
    prompt = f"""
    You are an AI assistant.

    Use ONLY the provided document context.
    Do NOT give generic answers.

    Question: {query}

    Instructions:
    - Explain clearly
    - Give examples if possible
    - Structure the answer in points
    """

    return query_engine.query(prompt)