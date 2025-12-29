import psycopg2
conn = psycopg2.connect(
    dbname="schooldb",
    user="postgres",
    password="anji",
    host="localhost",
    port="5432"
)
print("Connected!")
