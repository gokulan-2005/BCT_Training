from autogen import AssistantAgent
from config.llm_config import llm_config

risk_agent = AssistantAgent(
    name="RiskScorer",
    llm_config=llm_config,
    system_message="""
    Assign a risk level (Low, Medium, High).
    Consider:
    - Transaction amount
    - Country
    - Frequency
    """
)