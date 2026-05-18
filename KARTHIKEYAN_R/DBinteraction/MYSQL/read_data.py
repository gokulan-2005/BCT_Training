import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tommyshelby#18",
    database="mydb"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM students")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()