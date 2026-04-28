import pandas as pd
from app.pandas_service import analyze


def main():
    print("AI Log Analysis Tool (CLI)")
    print("=" * 40)

    df = pd.read_csv("data/logs.csv")

    print("Logs loaded successfully!")
    print(f"Loaded {len(df)} records\n")

    while True:
        query = input("Ask your question (or type 'exit'): ")

        if query.lower() == "exit":
            break

        print("\nAnalyzing...\n")

        result = analyze(df, query)

        print("\nResult:\n")
        print(result)
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()