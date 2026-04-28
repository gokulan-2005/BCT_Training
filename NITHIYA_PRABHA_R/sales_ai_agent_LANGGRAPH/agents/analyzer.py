from utils.llm import get_llm

llm = get_llm()

def analyze_lead(state):
    lead = state["lead"]

    prompt = f"""
    Analyze this lead:
    {lead}

    Extract:
    - Interest level
    - Budget
    - Company size
    """

    response = llm.invoke(prompt)

    return {"analysis": response.content}