from crewai import Task

def research_task(agent, topic):
    return Task(
        description=f"Find 5 simple bullet points about {topic} in easy English",
        expected_output=f"5 clear bullet points about {topic}",
        agent=agent
    )

def writing_task(agent, topic):
    return Task(
        description=f"Write a short paragraph about {topic} using the research",
        expected_output=f"A well-structured paragraph about {topic}",
        agent=agent
    )

def review_task(agent, topic):
    return Task(
        description=f"Improve the paragraph about {topic} and fix grammar",
        expected_output=f"A refined and corrected paragraph about {topic}",
        agent=agent
    )