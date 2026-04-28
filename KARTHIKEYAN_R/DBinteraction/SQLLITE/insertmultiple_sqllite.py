import sqlite3

conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

# multiple data
data = [
    ("Alice", 20),
    ("Bob", 23),
    ("Charlie", 22),
    ("David", 24)
]

# insert query
cursor.executemany(
    "INSERT INTO students (name, age) VALUES (?, ?)",
    data
)

conn.commit()

print("Multiple records inserted!")

conn.close()