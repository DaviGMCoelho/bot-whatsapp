from psycopg2.extensions import connection
from src.repositories.postgres.base_repository import PostgresBaseRepository

from src.domains.models.catalog import Catalog

class CatalogRepository(PostgresBaseRepository):
    def insert(self, conn: connection, catalog: Catalog):
        sql_query = self._load_query('catalog/queries/register_catalog.sql')

        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'name': catalog.name,
                'company_id': catalog.company,
                'active': catalog.active
            })
