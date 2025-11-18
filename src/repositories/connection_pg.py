import os
import psycopg2

class PostgresConn:
    def __init__(self):
        self.db_name = os.getenv("POSTGRES_DB")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.host = 'localhost'
        self.port = "5441"

    def get_connection(self):
        connection = psycopg2.connect(
            dbname = self.db_name,
            user = self.user,
            password = self.password,
            host = self.host,
            port = self.port
        )
        cursor = connection.cursor()
        return connection, cursor
