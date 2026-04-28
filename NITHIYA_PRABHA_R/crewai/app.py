import os
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

from crew import create_crew

def run():
    topic = input("Enter your topic: ")

    crew = create_crew(topic)
    result = crew.kickoff()

    print("\nFINAL OUTPUT\n")
    print(result)

if __name__ == "__main__":
    run()