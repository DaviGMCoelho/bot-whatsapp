from pathlib import Path

from src.database.connection_pg import PostgresConn

def init_database(connection: PostgresConn):
    schema_path = Path(__file__).parent / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as schema:
        schema_sql = schema.read()

    with connection.connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(schema_sql)
            conn.commit()
