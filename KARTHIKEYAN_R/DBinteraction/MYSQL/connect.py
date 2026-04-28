import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tommyshelby#18"
)

print("Connected successfully!")

conn.close()