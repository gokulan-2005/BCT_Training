from crewai import Agent
from utils.llm import get_llm

analyzer = Agent(
    role="Query Analyzer",
    goal="Understand the user query and identify intent",
    backstory="Expert in analyzing business questions",
    llm=get_llm(),
    verbose=True
)