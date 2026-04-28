import psycopg2

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Tommyshelby#18",
    database="mydb"
)

cursor = conn.cursor()

cursor.execute(
    "INSERT INTO students (name, age) VALUES (%s, %s)",
    ("Karthikeyan", 21)
)

conn.commit()

print("Data inserted!")

conn.close()