import psycopg2
from psycopg2 import sql
from database.connection import connection_config

class CarRepository:
  def create():
    conn = psycopg2.connect(**connection_config)
    cursor = conn.cursor()

    query = 'INSER INTO "car" (id, brand_id, model, year)'