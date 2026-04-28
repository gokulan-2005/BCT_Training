from autogen import AssistantAgent
from config.llm_config import llm_config

report_agent = AssistantAgent(
    name="ReportGenerator",
    llm_config=llm_config,
    system_message="""
    Generate a SHORT and CLEAR report.

    Format STRICTLY like this:

    Risk Level:
    <High/Medium/Low>

    Key Issues:
    - <point 1>
    - <point 2>

    Compliance Violations:
    - <point 1>
    - <point 2>

    Recommendation:
    - <short action>

    Keep output under 100 words.
    No explanations. No paragraphs.
    """
)