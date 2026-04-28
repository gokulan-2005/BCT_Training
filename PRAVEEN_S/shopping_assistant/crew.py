import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class SmartShoppingCrew():
    """Smart Shopping Assistant Crew"""

    # These point to the YAML files you already created
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        
        self.gemini_llm = LLM(
            model="gemini-3-flash-preview",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7
        )

    @agent
    def product_hunter(self) -> Agent:
        return Agent(
            config=self.agents_config['product_hunter'],
            llm=self.gemini_llm,
            tools=[SerperDevTool()], 
            verbose=True
        )

    @agent
    def review_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['review_analyst'],
            llm=self.gemini_llm,
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def final_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['final_auditor'],
            llm=self.gemini_llm,
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])

    @task
    def analysis_task(self) -> Task:
        return Task(config=self.tasks_config['analysis_task'])

    @task
    def final_report_task(self) -> Task:
        return Task(config=self.tasks_config['final_report_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )