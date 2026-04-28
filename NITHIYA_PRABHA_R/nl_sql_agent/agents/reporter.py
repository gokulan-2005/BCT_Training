from crewai import Agent
from utils.llm import get_llm

reporter = Agent(
    role="Report Generator",
    goal="Execute SQL and explain results clearly",
    backstory="Expert in data analysis and reporting",
    llm=get_llm(),
    verbose=True
)