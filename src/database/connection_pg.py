
import psycopg2
from contextlib import contextmanager

class PostgresConn:
    def __init__(self, db_name: str, user: str, password: str, host: str, port: int):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        return psycopg2.connect(
            dbname = self.db_name,
            user = self.user,
            password = self.password,
            host = self.host,
            port = self.port
        )

    @contextmanager
    def transaction(self):
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
