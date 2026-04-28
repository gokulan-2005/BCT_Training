from crewai import Agent

def get_researcher():
    return Agent(
        role="Researcher",
        goal="Find accurate and simple information",
        backstory="Expert in gathering useful data",
        llm="ollama/tinyllama", 
        verbose=True
    )

def get_writer():
    return Agent(
        role="Writer",
        goal="Write clear and structured content",
        backstory="Expert content writer",
        llm="ollama/tinyllama",  
        verbose=True
    )

def get_reviewer():
    return Agent(
        role="Reviewer",
        goal="Improve and correct the content",
        backstory="Expert reviewer",
        llm="ollama/tinyllama", 
        verbose=True
    )
