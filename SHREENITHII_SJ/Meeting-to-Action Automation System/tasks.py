from crewai import Task

def summarize_task(agent, notes):
    return Task(
        description=f"Summarize the following meeting notes clearly:\n{notes}",
        agent=agent,
        expected_output="A structured summary of the meeting"
    )

def extract_tasks(agent, summary):
    return Task(
        description=f"Extract all actionable tasks from this summary:\n{summary}",
        agent=agent,
        expected_output="List of action items"
    )

def assign_tasks(agent, tasks):
    return Task(
        description=f"Assign each task to a relevant person based on context:\n{tasks}",
        agent=agent,
        expected_output="Tasks with assigned owners"
    )

def plan_tasks(agent, assigned_tasks):
    return Task(
        description=f"Add priorities and deadlines to these tasks:\n{assigned_tasks}",
        agent=agent,
        expected_output="Final structured plan with priorities and deadlines"
    )