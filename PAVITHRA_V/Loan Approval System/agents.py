from crewai import Agent
from llm import get_llm
from tools import *

llm = get_llm()

credit_agent = Agent(
    role="Senior Credit Risk Analyst",
    goal="Evaluate applicant creditworthiness using financial indicators",
    backstory="""
    You are a senior banking analyst with expertise in credit scoring.

    Responsibilities:
    - Retrieve credit score using tool
    - Classify:
        >750 → Excellent
        650–750 → Good
        <650 → Poor

    Output format:
    {
      "credit_score": int,
      "category": "",
      "justification": ""
    }
    """,
    tools=[get_credit_score],
    llm=llm,
    verbose=False
)

income_agent = Agent(
    role="Income Verification Officer",
    goal="Assess repayment capacity",
    backstory="""
    You verify applicant income and evaluate repayment ability.

    Steps:
    - Fetch income
    - Estimate EMI affordability (<=40% income)

    Output JSON:
    {
      "monthly_income": float,
      "emi_capacity": float,
      "status": "SUFFICIENT | INSUFFICIENT"
    }
    """,
    tools=[get_income],
    llm=llm,
    verbose=False
)

risk_agent = Agent(
    role="Financial Risk Analyst",
    goal="Assess fraud and liability risk",
    backstory="""
    Use:
    - Fraud Detection Service
    - Loan History Service

    Evaluate:
    - Fraud risk
    - Debt exposure

    Output JSON:
    {
      "fraud_risk": "",
      "active_loans": int,
      "total_outstanding": float,
      "risk_level": ""
    }
    """,
    tools=[check_fraud, check_loans],
    llm=llm,
    verbose=False
)

decision_agent = Agent(
    role="Loan Approval Manager",
    goal="Make final loan approval decision",
    backstory="""
    Apply strict banking rules:

    REJECT if:
    - credit_score < 650
    - fraud_risk = HIGH_RISK
    - active_loans > 2
    - income insufficient

    Otherwise APPROVE

    Output STRICT JSON:
    {
      "decision": "APPROVED | REJECTED",
      "reason": "",
      "risk_level": ""
    }
    """,
    llm=llm,
    verbose=False
)