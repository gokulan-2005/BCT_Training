from crewai import Agent
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def jd_agent():
    return Agent(
        role="Job Description Analyst",
        goal="Extract required skills and responsibilities from job description",
        backstory="Expert in analyzing job roles and requirements",
        llm=llm
    )

def candidate_agent():
    return Agent(
        role="Candidate Analyst",
        goal="Analyze candidate profile and extract skills",
        backstory="Specialist in evaluating resumes and profiles",
        llm=llm
    )

def match_agent():
    return Agent(
        role="Match Evaluator",
        goal="Compare job requirements with candidate skills",
        backstory="Expert in identifying skill matches and gaps",
        llm=llm
    )

def decision_agent():
    return Agent(
        role="Hiring Decision Maker",
        goal="Provide hiring recommendation based on evaluation",
        backstory="Experienced in recruitment decision-making",
        llm=llm
    )