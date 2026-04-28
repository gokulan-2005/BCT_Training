from dotenv import load_dotenv
from db import init_db, run_query
from agents import nl_to_sql, insight_agent

load_dotenv()

def main():
    init_db()

    print("\nLog Intelligence System Ready\n")

    while True:
        question = input("Ask about logs: ")

        if question.lower() == "exit":
            break

        sql = nl_to_sql(question)

        print("\nSQL:", sql)

        try:
            result = run_query(sql)
            print("\nResult:", result)

            insight = insight_agent(question, result)

            print("\nInsight:")
            print(insight)
            print("\n" + "-"*50)

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()