from database.db import get_db
from agents.table_selector import get_relevant_tables
from agents.query_generator import generate_query
from agents.answer_generator import generate_answer

def run_sql_agent(question):
    db = get_db()

    print("🔍 Finding relevant tables...")
    tables = get_relevant_tables(question)

    print("📊 Fetching schema...")
    schema = db.get_table_info(tables)

    print("🧾 Generating SQL query...")
    query = generate_query(question, schema)
    print("Generated Query:", query)

    print("⚡ Executing query...")
    result = db.run(query)

    print("💬 Generating answer...")
    answer = generate_answer(question, result)

    return answer


if __name__ == "__main__":
    q = input("Ask your question: ")
    response = run_sql_agent(q)
    print("\nFinal Answer:", response)