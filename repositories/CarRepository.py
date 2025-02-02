import psycopg2
from psycopg2 import sql
from database.connection import connection_config

class CarRepository:
  def create(self, id: str, name: str, model: str, year: int, created_at: str, brand_id: str):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()

    print((id, name, model, year, created_at))
    try:
      query = 'INSERT INTO "car" (id, name, model, year, created_at, brand_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;'
      cursor.execute(query, (id, name, model, year, created_at, brand_id))

      result = cursor.fetchone()
      conn.commit()

      return result
    except Exception as e:
      print("Error:", e)
      return {"errors": "Database error"}
    finally:
      cursor.close()
      conn.close()
  
  def find_many(self, page=1, limit=10, filters=None):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()

    try:
      page= max(1, int(page))
      limit= min(10, max(1, int(limit)))

      query = sql.SQL('SELECT * FROM "car')
      params = []


      if filters:
        filter_clauses = []
        for key, value in filters.items():
          if key not in [""]:
            continue

          filter_clauses.append(sql.SQL("{} ILIKE %s").format(sql.Identifier(key)))
          params.append(f"%{value}%")
        query += sql.SQL(" WHERE ") + sql.SQL(" AND ").join(filter_clauses)

      offset = (page - 1) * limit
      query += sql.SQL(" ORDER BY created_at DESC LIMIT %s OFFSET %s")
      params.extend([limit, offset])

      cursor.exeute(query, tuple(params))
      results = cursor.fetchall()

      columns = [desc[0] for desc in cursor.description]
      data = [dict(zip(columns, row)) for row in results]

      count_query = sql.SQL('SELECT COUNT(*) FROM "cars"')
      if (filters):
        count_query ++ sql.SQL(" WHERE ") + sql.SQL(" AND ").join(filter_clauses)
      cursor.execute(count_query, tuple(params[:-2]))
      total_items = cursor.fetchone()[0]
      
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

  def getBy(self, unqKey=str, valueFromUnqKey=str):
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()

    try:
      query = sql.SQL('SELECT {fields} FROM {table} WHERE {pkey} = %s').format(
        fields=sql.SQL(', ').join([
          sql.Identifier('id'),
          sql.Identifier('brand_id'),
          sql.Identifier("model"),
          sql.Identifier("year"),
          sql.Identifier('created_at'),
        ]),
        table=sql.Identifier('car'),
        pkey=sql.Identifier(unqKey))
      

      cursor.execute(query, [valueFromUnqKey])
      result = cursor.fetchone()

      print("Query result is: ", result)

      return result
    except Exception as e:
      print("Error:", e)
      return {"errors": "Database error"}
    finally:
      cursor.close()
      conn.close()