from crewai import Crew, Process
from agents import summarizer_agent, action_extractor_agent, assignment_agent, planner_agent
from tasks import summarize_task, extract_tasks, assign_tasks, plan_tasks

def main():
    print("\nMeeting-to-Action System Ready\n")

    notes = input("Enter meeting notes:\n")

    summarizer = summarizer_agent()
    extractor = action_extractor_agent()
    assigner = assignment_agent()
    planner = planner_agent()

    task1 = summarize_task(summarizer, notes)
    task2 = extract_tasks(extractor, task1)
    task3 = assign_tasks(assigner, task2)
    task4 = plan_tasks(planner, task3)

    crew = Crew(
        agents=[summarizer, extractor, assigner, planner],
        tasks=[task1, task2, task3, task4],
        process=Process.sequential
    )

    result = crew.kickoff()

    print("\nFinal Output:\n")
    print(result)

if __name__ == "__main__":
    main()