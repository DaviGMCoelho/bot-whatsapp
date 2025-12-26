from pathlib import Path
from abc import ABC

class PostgresBaseRepository(ABC):
    def __init__(self):
        self.queries_path = Path(__file__).parent

    def _load_query(self, filename: str):
        with open(self.queries_path / filename, 'r', encoding='utf-8') as query:
            return query.read()
