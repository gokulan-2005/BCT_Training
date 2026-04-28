from crewai import Crew, Process
from agents import jd_agent, candidate_agent, match_agent, decision_agent
from tasks import jd_task, candidate_task, match_task, decision_task

def main():
    print("\nJob Evaluation System Ready\n")

    jd = input("Enter Job Description:\n")
    profile = input("\nEnter Candidate Profile:\n")

    jd_analyzer = jd_agent()
    candidate_analyzer = candidate_agent()
    matcher = match_agent()
    decider = decision_agent()

    task1 = jd_task(jd_analyzer, jd)
    task2 = candidate_task(candidate_analyzer, profile)
    task3 = match_task(matcher, "{task1.output}", "{task2.output}")
    task4 = decision_task(decider, "{task3.output}")

    crew = Crew(
        agents=[jd_analyzer, candidate_analyzer, matcher, decider],
        tasks=[task1, task2, task3, task4],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    print("\nFinal Result:\n")
    print(result)

if __name__ == "__main__":
    main()