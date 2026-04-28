import sqlite3

def init_db():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        timestamp TEXT,
        service TEXT,
        level TEXT,
        message TEXT,
        response_time REAL
    )
    """)

    cursor.execute("DELETE FROM logs")

    data = [
        ("10:00", "auth", "ERROR", "timeout", 2.5),
        ("10:05", "auth", "ERROR", "timeout", 3.0),
        ("11:00", "payment", "INFO", "success", 1.2),
        ("12:00", "auth", "ERROR", "failure", 2.8),
        ("13:00", "payment", "ERROR", "failed", 2.0)
    ]

    cursor.executemany(
        "INSERT INTO logs VALUES (?, ?, ?, ?, ?)", data
    )

    conn.commit()
    conn.close()

def run_query(query):
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result