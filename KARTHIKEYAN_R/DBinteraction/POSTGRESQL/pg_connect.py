import psycopg2

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Tommyshelby#18",
    database="postgres"   
)

print("Connected to PostgreSQL!")

conn.close()