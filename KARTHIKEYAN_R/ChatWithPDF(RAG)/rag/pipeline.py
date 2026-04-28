from config import GROQ_MODEL, groq_client
from rag.retriever import retrieve

def generate_answer(query):
    docs = retrieve(query)

    if not docs:
        return "⚠️ No relevant context found."

    context = "\n\n".join(docs)
    context = context[:2000]

    prompt = f"""
    You are an AI assistant.

    Context:
    {context}

    Question:
    {query}

    Answer clearly.
    """

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "Helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content