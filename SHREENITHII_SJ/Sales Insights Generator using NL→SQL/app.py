from dotenv import load_dotenv
from db import init_db, run_query
from agents import nl_to_sql_agent, insight_agent

load_dotenv()

def main():
    init_db()

    print("\nSales Insight System Ready\n")

    while True:
        question = input("Ask about sales (or type exit): ")

        if question.lower() == "exit":
            break

        sql = nl_to_sql_agent(question)

        print("\nGenerated SQL:")
        print(sql)

        try:
            result = run_query(sql)
            print("\nRaw Data:", result)

            insight = insight_agent(question, result)

            print("\nInsight:")
            print(insight)
            print("\n" + "-"*50)

        except Exception as e:
            print("Error executing SQL:", e)

if __name__ == "__main__":
    main()