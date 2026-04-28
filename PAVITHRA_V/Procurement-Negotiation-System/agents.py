from autogen_agentchat.agents import AssistantAgent
from config import model_client

# Extractor
extractor = AssistantAgent(
    name="Extractor",
    model_client=model_client,
    system_message="""
    Extract structured data ONLY.

    INPUT: raw text
    OUTPUT (STRICT JSON ONLY):
    [
      {"vendor": "...", "price": number, "delivery_days": number}
    ]

    NO explanation.
    """
)

# Risk Agent
risk_agent = AssistantAgent(
    name="RiskAgent",
    model_client=model_client,
    system_message="""
    INPUT: JSON from Extractor

    TASK:
    Calculate risk score (0-10)

    OUTPUT (STRICT JSON):
    [
      {"vendor": "...", "risk_score": number, "reason": "..."}
    ]

    DO NOT repeat extraction.
    DO NOT explain steps.
    """
)

# Comparison Agent
comparison_agent = AssistantAgent(
    name="ComparisonAgent",
    model_client=model_client,
    system_message="""
    INPUT:
    - vendor data
    - risk data

    TASK:
    Rank vendors

    OUTPUT (STRICT JSON):
    [
      {"rank": 1, "vendor": "...", "reason": "..."},
      {"rank": 2, ...}
    ]

    DO NOT recompute risk.
    """
)

# Negotiation Agent
negotiation_agent = AssistantAgent(
    name="NegotiationAgent",
    model_client=model_client,
    system_message="""
    INPUT: top vendor

    TASK:
    Reduce cost by 10%

    OUTPUT:
    {
      "vendor": "...",
      "original_price": number,
      "negotiated_price": number,
      "email": "professional email"
    }

    NO analysis.
    """
)

# Decision Agent 
decision_agent = AssistantAgent(
    name="DecisionAgent",
    model_client=model_client,
    system_message="""
    INPUT:
    - ranked vendors
    - negotiation result

    TASK:
    Produce FINAL_DECISION

    OUTPUT (STRICT JSON):
    {
      "vendor": "...",
      "final_price": number,
      "justification": "...",
      "risk_summary": "..."
    }

    NO explanation outside JSON.
    """
)

# Validator Agent 
validator_agent = AssistantAgent(
    name="ValidatorAgent",
    model_client=model_client,
    system_message="""
    INPUT: FINAL_DECISION JSON

    VALIDATE:
    - Is best vendor logically correct?
    - Is risk considered?
    - Is price optimized?

    OUTPUT:
    APPROVED
    or
    REJECTED: <reason>

    Be strict. Do NOT approve weak logic.
    """
)