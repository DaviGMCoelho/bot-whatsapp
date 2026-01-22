from psycopg2.extensions import connection
from src.repositories.postgres.base_repository import PostgresBaseRepository

from src.domains.models.catalog import Catalog

class CatalogRepository(PostgresBaseRepository):
    def __init__(self):
        super().__init__()
        self.ALLOWED_FIELDS = {'name', 'active'}

    def insert(self, conn: connection, catalog: Catalog):
        sql_query = self._load_query('catalog/queries/register_catalog.sql')

        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'code': catalog.code,
                'name': catalog.name,
                'company_id': catalog.company,
                'active': catalog.active
            })

    def update(self, conn: connection, catalog_code: str, data: dict):
        query_raw = self._load_query('catalog/queries/update_catalog.sql')
        sql_query, params = self._build_update_query(query_raw, self.ALLOWED_FIELDS, catalog_code, data)

        with conn.cursor() as cursor:
            cursor.execute(sql_query, params)