import sqlite3

def init_db():
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        monthly_income REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loans (
        loan_id TEXT,
        user_id TEXT,
        amount REAL,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        txn_id TEXT,
        user_id TEXT,
        amount REAL
    )
    """)

    # Seed data
    cursor.executemany("INSERT OR REPLACE INTO customers VALUES (?, ?, ?)", [
        ("USER001", "Arun", 60000),
        ("USER002", "Ravi", 25000)
    ])

    cursor.executemany("INSERT INTO loans VALUES (?, ?, ?, ?)", [
        ("L1", "USER001", 50000, "ACTIVE"),
        ("L2", "USER001", 30000, "ACTIVE"),
        ("L3", "USER002", 20000, "CLOSED")
    ])

    cursor.executemany("INSERT INTO transactions VALUES (?, ?, ?)", [
        ("T1", "USER001", 5000),
        ("T2", "USER001", 7000),
        ("T3", "USER001", 120000),
        ("T4", "USER002", 3000)
    ])

    conn.commit()
    conn.close()