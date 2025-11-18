from abc import ABC
from src.repositories.connection_pg import PostgresConn

class PostgresBaseRepository(ABC):
    def __init__(self):
        self._connection = PostgresConn()

    def _load_query(self, query_path: str):
        with open(query_path, 'r', encoding='utf-8') as query:
            return query.read()
