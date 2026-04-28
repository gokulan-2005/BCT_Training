import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tommyshelby#18",
    database="mydb"
)

cursor = conn.cursor()

sql = "INSERT INTO students (name, age) VALUES (%s, %s)"
values = [
    ("Karthikeyan", 21),
    ("Arun", 22),
    ("Vijay", 20)
]

cursor.executemany(sql, values)
conn.commit()

print("Data inserted successfully!")

conn.close()