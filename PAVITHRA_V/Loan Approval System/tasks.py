from crewai import Task
from agents import *
def create_tasks(user_id: str):

    credit_task = Task(
        description=f"""
        Perform credit evaluation for user_id: {user_id}.

        Instructions:
        - Use the "Credit Score Service" tool to retrieve the credit score.
        - Classify the score into:
            > 750 → Excellent
            650–750 → Good
            < 650 → Poor

        Output Requirements (STRICT JSON):
        {{
            "user_id": "{user_id}",
            "credit_score": int,
            "category": "Excellent | Good | Poor",
            "justification": "Explain reasoning based on score"
        }}
        """,
        agent=credit_agent,
        expected_output="Structured JSON with credit score and classification"
    )

    income_task = Task(
        description=f"""
        Perform income verification for user_id: {user_id}.

        Instructions:
        - Use the "Income Service" tool to fetch monthly income.
        - DO NOT call any external tool for EMI calculation.
        - Compute EMI affordability internally as:
              emi_capacity = monthly_income * 0.4

        Decision Rules:
        - If emi_capacity >= 20000 → SUFFICIENT
        - Else → INSUFFICIENT

        Output Requirements (STRICT JSON):
        {{
            "user_id": "{user_id}",
            "monthly_income": float,
            "emi_capacity": float,
            "status": "SUFFICIENT | INSUFFICIENT"
        }}

        IMPORTANT:
        - Only use the "Income Service" tool
        - Do not invent or call any other tools
        """,
        agent=income_agent,
        expected_output="Structured JSON with income and repayment capacity"
    )

    risk_task = Task(
        description=f"""
        Perform financial risk assessment for user_id: {user_id}.

        Instructions:
        - Use "Fraud Detection Service" to determine fraud risk.
        - Use "Loan History Service" to fetch:
            - number of active loans
            - total outstanding amount

        Risk Rules:
        - HIGH_RISK fraud → High risk
        - active_loans > 2 → High risk
        - otherwise → Medium/Low risk

        Output Requirements (STRICT JSON):
        {{
            "user_id": "{user_id}",
            "fraud_risk": "LOW_RISK | MEDIUM_RISK | HIGH_RISK",
            "active_loans": int,
            "total_outstanding": float,
            "risk_level": "LOW | MEDIUM | HIGH"
        }}
        """,
        agent=risk_agent,
        expected_output="Structured JSON with fraud and loan risk analysis"
    )

    decision_task = Task(
        description=f"""
        Make final loan approval decision for user_id: {user_id}.

        You will receive outputs from:
        - Credit Analysis
        - Income Verification
        - Risk Assessment

        Apply STRICT RULES:

        REJECT if ANY:
        - credit_score < 650
        - fraud_risk == HIGH_RISK
        - active_loans > 2
        - status == INSUFFICIENT

        OTHERWISE:
        → APPROVE

        Output Requirements (STRICT JSON ONLY):
        {{
            "user_id": "{user_id}",
            "decision": "APPROVED | REJECTED",
            "reason": "Detailed explanation combining all factors",
            "risk_level": "LOW | MEDIUM | HIGH"
        }}

        DO NOT output anything outside JSON.
        """,
        agent=decision_agent,
        expected_output="Final structured decision in JSON"
    )

    return [
        credit_task,
        income_task,
        risk_task,
        decision_task
    ]