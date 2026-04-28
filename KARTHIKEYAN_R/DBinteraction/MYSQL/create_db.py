import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tommyshelby#18"
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE mydb")

print("Database created successfully!")

conn.close()