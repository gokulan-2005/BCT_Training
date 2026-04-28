import sqlite3

conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", ("Karthikeyan", 21))

conn.commit()

print("Data inserted!")

conn.close()