import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tommyshelby#18",
    database="mydb"
)

cursor = conn.cursor()

sql = "UPDATE students SET age = %s WHERE name = %s"
values = (25, "Karthikeyan")

cursor.execute(sql, values)
conn.commit()

print("Data updated!")

conn.close()