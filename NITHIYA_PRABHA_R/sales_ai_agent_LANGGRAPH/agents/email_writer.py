from utils.llm import get_llm

llm = get_llm()

def generate_email(state):
    lead = state["lead"]
    qualification = state["qualification"]

    prompt = f"""
    Write a professional sales email.

    Lead: {lead}
    Qualification: {qualification}

    Keep it short and persuasive.
    """

    response = llm.invoke(prompt)

    return {"email": response.content}