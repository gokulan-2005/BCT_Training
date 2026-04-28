import psycopg2

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Tommyshelby#18",
    database="postgres"
)

conn.autocommit = True
cursor = conn.cursor()

cursor.execute("CREATE DATABASE mydb")

print("Database created!")

conn.close()