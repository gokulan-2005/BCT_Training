from autogen import AssistantAgent
from config.llm_config import llm_config

compliance_agent = AssistantAgent(
    name="ComplianceChecker",
    llm_config=llm_config,
    system_message="""
    Check compliance rules:
    - Transactions > 100000 are risky
    - Unknown countries are suspicious
    - Flag violations clearly
    """
)