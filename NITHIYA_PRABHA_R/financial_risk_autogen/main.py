import json
from autogen import UserProxyAgent

from agents.transaction_agent import transaction_agent
from agents.risk_agent import risk_agent
from agents.compliance_agent import compliance_agent
from agents.report_agent import report_agent

with open("data/sample_transaction.json") as f:
    transactions = json.load(f)

input_data = json.dumps(transactions, indent=2)

#initializing user proxy agent to orchestrate the workflow
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    code_execution_config=False
)

print("\n STEP 1: Transaction Analysis\n")

res1 = user_proxy.initiate_chat(
    transaction_agent,
    message=f"Analyze these transactions:\n{input_data}",
    max_turns=1
)

analysis_output = res1.summary

print("\n STEP 2: Risk Scoring\n")

res2 = user_proxy.initiate_chat(
    risk_agent,
    message=f"Based on this analysis:\n{analysis_output}\nAssign risk levels.",
    max_turns=1
)

risk_output = res2.summary

print("\n STEP 3: Compliance Check\n")

res3 = user_proxy.initiate_chat(
    compliance_agent,
    message=f"Check compliance issues based on:\n{risk_output}",
    max_turns=1
)

compliance_output = res3.summary

print("\nSTEP 4: Final Report\n")

res4 = user_proxy.initiate_chat(
    report_agent,
    message="Generate a concise risk report in strict format.",
    max_turns=1
)

print("\nFINAL OUTPUT:\n")
print(res4.summary)