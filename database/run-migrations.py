import os 
import psycopg2
from psycopg2 import sql 

db_config = {
  'dbname':'mydatabase',
  'user':'user',
  'password':'password',
  'host':'localhost',
  'port':'5432'
}

script_dir = os.path.dirname(os.path.abspath(__file__))
migrations_dir = os.path.join(script_dir, 'migrations')

def run_migrations():
  try:
    # Connect on the database
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    print(os.listdir(migrations_dir))
    migrations_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith(".sql")])


    for migration_file in migrations_files:
      with open(os.path.join(migrations_dir, migration_file), 'r') as file:
        sql_script = file.read()
        print(f"Executando {migration_file}")
        cursor.execute(sql_script)
        conn.commit()
        print(f"{migration_file} executado com sucesso")
      
    # close the nonnection
    cursor.close()
    conn.close()
  
  except Exception as e:
    print(f"Error when execute migration: {e}")
  finally:
    if conn is not None:
      conn.close()

run_migrations()