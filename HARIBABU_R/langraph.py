from langgraph.graph import StateGraph
from langchain.chat_models import ChatOpenAI
from typing import TypedDict
import pandas as pd
import os

# Load dataset
df = pd.read_csv("resume_dataset.csv")

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Define state
class ResumeState(TypedDict):
    resume: str
    parsed: str
    match: str
    score: str

# Nodes (functions)

def parse_resume(state: ResumeState):
    prompt = f"Extract skills and experience:\n{state['resume']}"
    response = llm.invoke(prompt)
    return {"parsed": response.content}

def match_job(state: ResumeState):
    prompt = f"Match this to Data Scientist role:\n{state['parsed']}"
    response = llm.invoke(prompt)
    return {"match": response.content}

def rank_candidate(state: ResumeState):
    prompt = f"Score candidate (1-10):\n{state['match']}"
    response = llm.invoke(prompt)
    return {"score": response.content}

# Build graph
graph = StateGraph(ResumeState)

graph.add_node("parser", parse_resume)
graph.add_node("matcher", match_job)
graph.add_node("ranker", rank_candidate)

graph.set_entry_point("parser")

graph.add_edge("parser", "matcher")
graph.add_edge("matcher", "ranker")

app = graph.compile()

# Run for dataset
for _, row in df.iterrows():
    result = app.invoke({"resume": row["Resume"]})
    print("\nResult:", result)