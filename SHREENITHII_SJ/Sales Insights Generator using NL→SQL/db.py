import sqlite3

def init_db():
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer TEXT,
        product TEXT,
        region TEXT,
        amount INTEGER
    )
    """)

    cursor.execute("DELETE FROM sales")

    data = [
        ("Alice", "Laptop", "South", 50000),
        ("Bob", "Phone", "North", 20000),
        ("Charlie", "Laptop", "East", 70000),
        ("David", "Tablet", "South", 15000),
        ("Eva", "Phone", "West", 30000),
    ]

    cursor.executemany(
        "INSERT INTO sales (customer, product, region, amount) VALUES (?, ?, ?, ?)",
        data
    )

    conn.commit()
    conn.close()

def run_query(query):
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result