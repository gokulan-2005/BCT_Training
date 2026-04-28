from crewai import Agent
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def summarizer_agent():
    return Agent(
        role="Meeting Summarizer",
        goal="Convert raw meeting notes into a clear structured summary",
        backstory="Expert in understanding and summarizing discussions clearly",
        llm=llm
    )

def action_extractor_agent():
    return Agent(
        role="Action Extractor",
        goal="Identify actionable tasks from meeting discussions",
        backstory="Skilled at detecting responsibilities and tasks from conversations",
        llm=llm
    )

def assignment_agent():
    return Agent(
        role="Assignment Manager",
        goal="Assign tasks to appropriate people based on context",
        backstory="Expert in task delegation and responsibility mapping",
        llm=llm
    )

def planner_agent():
    return Agent(
        role="Planning Specialist",
        goal="Add priorities and deadlines to tasks",
        backstory="Focused on organizing work with timelines and priorities",
        llm=llm
    )