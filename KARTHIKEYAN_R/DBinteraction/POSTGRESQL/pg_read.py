import psycopg2

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Tommyshelby#18",
    database="mydb"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM students")

for row in cursor.fetchall():
    print(row)

conn.close()