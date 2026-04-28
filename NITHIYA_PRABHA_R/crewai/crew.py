from crewai import Crew
from agents import get_researcher, get_writer, get_reviewer
from tasks import research_task, writing_task, review_task

def create_crew(topic):
    researcher = get_researcher()
    writer = get_writer()
    reviewer = get_reviewer()

    task1 = research_task(researcher, topic)
    task2 = writing_task(writer, topic)
    task3 = review_task(reviewer, topic)

    crew = Crew(
        agents=[researcher, writer, reviewer],
        tasks=[task1, task2, task3],
        verbose=True
    )

    return crew