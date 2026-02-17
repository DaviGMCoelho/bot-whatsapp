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
        sql_query, params = self._build_update_query(query_raw, self.ALLOWED_FIELDS, data)
        params['code']: catalog_code

        with conn.cursor() as cursor:
            cursor.execute(sql_query, params)


    def change_state(self, conn: connection, company_id: int, catalog_code: str, active: bool):
        sql_query = self._load_query('catalog/queries/change_catalog_state.sql')

        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'active': active,
                'code': catalog_code,
                'company_id': company_id
            })
