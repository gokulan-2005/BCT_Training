from crew import create_crew

def main():
    print(" AI Data Analyst (CrewAI + Groq)")
    print("Type 'exit' to quit\n")

    while True:
        query = input("Ask your question: ")

        if query.lower() == "exit":
            print(" Exiting...")
            break

        try:
            crew = create_crew(query)
            result = crew.kickoff()

            print("\n Final Answer:")
            print(result)

        except Exception as e:
            print("\nError:", str(e))


if __name__ == "__main__":
    main()