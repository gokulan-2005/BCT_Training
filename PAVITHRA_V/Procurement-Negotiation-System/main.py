import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.conditions import TextMentionTermination

from agents import (
    extractor,
    risk_agent,
    comparison_agent,
    negotiation_agent,
    decision_agent,
    validator_agent,
)

termination = TextMentionTermination("APPROVED")

team = RoundRobinGroupChat(
    participants=[
        extractor,
        risk_agent,
        comparison_agent,
        negotiation_agent,
        decision_agent,
        validator_agent,
    ],
    max_turns=12,
    termination_condition=termination,
)

task = """
    We received vendor quotes:

    Vendor A: price 1000 USD, delivery 10 days
    Vendor B: price 850 USD, delivery 20 days
    Vendor C: price 1100 USD, delivery 5 days

    Steps:
    1. Extract structured data
    2. Evaluate risk
    3. Compare vendors
    4. Negotiate best option
    5. Provide FINAL_DECISION
    """

async def run():
    final_decision = None

    try:
        stream = team.run_stream(
            task=TextMessage(content=task, source="user")
        )

        async for msg in stream:
            print(f"\n[{msg.source}]")
            print(msg.content)

            # Capture DecisionAgent output
            if msg.source == "DecisionAgent":
                final_decision = msg.content

            # Stop cleanly when approved
            if msg.source == "ValidatorAgent" and "APPROVED" in msg.content:
                print("\n FINAL OUTPUT:")
                print(final_decision)
                break

    except Exception as e:
        print("Handled error:", e)

if __name__ == "__main__":
    asyncio.run(run())