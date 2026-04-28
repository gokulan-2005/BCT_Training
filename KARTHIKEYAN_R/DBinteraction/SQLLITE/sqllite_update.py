import sqlite3

conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

cursor.execute("UPDATE students SET age = ? WHERE name = ?", (25, "Karthikeyan"))

conn.commit()

print("Updated!")

conn.close()