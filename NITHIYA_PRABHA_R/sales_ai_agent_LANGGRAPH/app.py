import json
from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.analyzer import analyze_lead
from agents.qualifier import qualify_lead
from agents.email_writer import generate_email


class LeadState(TypedDict):
    lead: dict
    analysis: str
    qualification: str
    email: str


graph = StateGraph(LeadState)

graph.add_node("analyze", analyze_lead)
graph.add_node("qualify", qualify_lead)
graph.add_node("email", generate_email)

graph.set_entry_point("analyze")

graph.add_edge("analyze", "qualify")

def route(state):
    if state["qualification"] == "Hot":
        return "email"
    else:
        return END

graph.add_conditional_edges("qualify", route)

graph.add_edge("email", END)

app = graph.compile()

with open("data/leads.json", "r") as file:
    leads = json.load(file)


hot_count = 0

print("\nHOT LEADS OUTPUT\n")

for lead in leads:
    result = app.invoke({"lead": lead})

    if result["qualification"] == "Hot":
        hot_count += 1

        print("\n==============================")
        print("   HOT LEAD FOUND")
        print("==============================")

        print(f"Name         : {lead['name']}")
        print(f"Company      : {lead['company']}")
        print(f"Qualification: {result['qualification']}")

        if "email" in result:
            print("\n--- Email ---")
            print(result["email"])

print("\n==============================")
print(f"Total HOT Leads: {hot_count}")
print("==============================")