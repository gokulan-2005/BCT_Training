from crewai import Agent
from utils.llm import get_llm

sql_generator = Agent(
    role="SQL Generator",
    goal="Convert natural language into SQL query",
    backstory="Expert in MySQL and joins",
    llm=get_llm(),
    verbose=True
)