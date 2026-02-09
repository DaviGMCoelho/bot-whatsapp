from pathlib import Path
from abc import ABC

class PostgresBaseRepository(ABC):
    def __init__(self):
        self.queries_path = Path(__file__).parent

    def _load_query(self, filename: str):
        with open(self.queries_path / filename, 'r', encoding='utf-8') as query:
            return query.read()
        
    def _build_update_query(self, sql_query: str, allowed_fields: set, data: dict):
        set_clauses = []
        params = {}

        for field, value in data.items():
            if field not in allowed_fields:
                continue
            set_clauses.append(f'{field} = %({field})s')
            params[field] = value
        if not set_clauses:
            raise ValueError("Nenhum campo válido para atualização")

        set_clause = ', '.join(set_clauses)
        new_query = sql_query.replace("{{set_clause}}", set_clause)

        return new_query, params
