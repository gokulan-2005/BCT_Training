import sys

from .crew import run_crew


def run() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    topic = input("Enter topic: ").strip()
    if not topic:
        print("Please enter a topic.")
        return

    result = run_crew(topic)
    print(result)

if __name__ == "__main__":
    run()
