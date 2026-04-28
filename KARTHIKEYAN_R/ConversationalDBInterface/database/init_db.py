import sqlite3

conn = sqlite3.connect("sample.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    product TEXT,
    amount INTEGER
)
""")

cursor.execute("INSERT INTO sales (product, amount) VALUES ('Laptop', 1000)")
cursor.execute("INSERT INTO sales (product, amount) VALUES ('Phone', 500)")

conn.commit()
conn.close()

print("✅ Database created successfully!")