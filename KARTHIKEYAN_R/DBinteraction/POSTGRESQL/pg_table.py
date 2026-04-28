import psycopg2

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Tommyshelby#18",
    database="mydb"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INT
)
""")

conn.commit()

print("Table created!")

conn.close()