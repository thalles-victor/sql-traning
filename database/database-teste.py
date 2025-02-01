import uuid
import psycopg2
import datetime

conn = psycopg2.connect(
    dbname="mydatabase",
    user="user",
    password="password",
    host="localhost",  # ou o IP do servidor
    port="5432"  # porta padrão do PostgreSQL)
)

cursor = conn.cursor()

uuid_str = str(uuid.uuid4())

cursor.execute('INSERT INTO "user" (id, name, email, password, date) VALUES (%s, %s, %s, %s, %s) RETURNING *;', (uuid_str, "jhon", "jhon@gmail.com", "#jhonpassw12", datetime.date(2005, 11, 18)))

result = cursor.execute('SELECT * FROM "user"')
print(cursor.fetchall())

conn.commit()



cursor.close()
conn.close()