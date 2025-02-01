import psycopg2
from psycopg2 import sql
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
  
  def find_many(self, page=1, limit=10, filters=None):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()

    try:
      page = max(1, int(page))
      limit = min(10, max(1, int(limit)))


      query = sql.SQL('SELECT * FROM "brand"')
      params = []

      if filters:
        filter_clauses = []
        for key, value in filters.items():
          if key not in ["name", "description"]:
            continue

          filter_clauses.append(sql.SQL("{} ILIKE %s").format(sql.Identifier(key)))
          params.append(f"%{value}%")
        query += sql.SQL(" WHERE ") + sql.SQL(" AND ").join(filter_clauses)
      
      # pagination
      offset = (page - 1) * limit
      query += sql.SQL(" ORDER BY created_at DESC LIMIT %s OFFSET %s")
      params.extend([limit, offset])

      cursor.execute(query, tuple(params))
      results = cursor.fetchall()

      # Obtém os nomes das colunas
      colunas = [desc[0] for desc in cursor.description]

      # Converte a lista de tuplas para uma lista de dicionários
      data = [dict(zip(colunas, row)) for row in results]


      # count all registers without pagination
      count_query = sql.SQL('SELECT COUNT(*) FROM "brand"')
      if filters:
        count_query += sql.SQL(" WHERE ") + sql.SQL(" AND ").join(filter_clauses)
      cursor.execute(count_query, tuple(params[:-2]))
      total_items = cursor.fetchone()[0]
      
      cursor.close()
      conn.close()

      print(results)
      
      return {
        "data": data,
        "total": total_items,
        "page": page,
        "limit": limit,
        "total_pages": (total_items + limit -1) // limit
      }
    except Exception as e:
      print("Error:", e)
      return {"errors": "Database error"}
    finally:
      cursor.close()
      conn.close()
