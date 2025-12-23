from pathlib import Path
from abc import ABC
from src.repositories.connection_pg import PostgresConn

class PostgresBaseRepository(ABC):
    def __init__(self):
        self._db = PostgresConn()

    def get_connection(self):
        return self._db.get_connection()

    def _load_query(self, relative_path: str):
        base_dir = Path(__file__).resolve().parents[3]
        query_path = base_dir / relative_path

        with open(query_path, 'r', encoding='utf-8') as query:
            return query.read()
