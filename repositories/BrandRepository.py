import psycopg2
from database.connection import connection_config

class BrandRepository:
  def create(self, id: str, name: str, description: str, created_at: str):
    conn = psycopg2.connect(**connection_config)
    cursor= conn.cursor()

    query = 'INSERT INTO "brand" (id, name, description, created_at) VALUES (%s, %s, %s, %s) RETURNING *;'
    cursor.execute(query, (id, name, description, created_at))

    result = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    return result