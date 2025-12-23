import time
import os
import psycopg2

class PostgresConn:
    def __init__(self):
        self.db_name = os.getenv("POSTGRES_DB")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.host = os.getenv("POSTGRES_HOST")
        self.port = int(os.getenv("POSTGRES_PORT"))

    def get_connection(self):
        return psycopg2.connect(
            dbname = self.db_name,
            user = self.user,
            password = self.password,
            host = self.host,
            port = self.port
        )
