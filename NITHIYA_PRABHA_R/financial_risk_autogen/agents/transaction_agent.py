from autogen import AssistantAgent
from config.llm_config import llm_config

transaction_agent = AssistantAgent(
    name="TransactionAnalyzer",
    llm_config=llm_config,
    system_message="""
    You analyze financial transactions.
    Identify unusual patterns like:
    - Large transactions
    - Foreign transfers
    - Frequent transactions
    """
)