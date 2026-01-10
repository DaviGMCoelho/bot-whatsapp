from psycopg2.extensions import connection
from src.repositories.postgres.base_repository import PostgresBaseRepository

from src.domains.models.items import Items

class ItemRepository(PostgresBaseRepository):
    def insert(self, conn: connection, item: Items):
        sql_query = self._load_query('item/queries/register_item.sql')

        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'catalog_id': item.catalog,
                'active': item.active
            })
