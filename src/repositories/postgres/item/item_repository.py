from psycopg2.extensions import connection
from src.repositories.postgres.base_repository import PostgresBaseRepository

from src.domains.models.item import Item

class ItemRepository(PostgresBaseRepository):
    def __init__(self):
        super().__init__()
        self.ALLOWED_FIELDS = {'name', 'description', 'price', 'catalog_id', 'active'}

    def insert(self, conn: connection, item: Item):
        sql_query = self._load_query('item/queries/register_item.sql')
        print('passou pelo insert')
        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'code': item.code,
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'catalog_id': item.catalog,
                'active': item.active
            })

    def update(self, conn: connection, item_code: str, data: dict):
        query_raw = self._load_query('item/queries/update_item.sql')
        sql_query, params = self._build_update_query(query_raw, self.ALLOWED_FIELDS, 'code', item_code, data)

        with conn.cursor() as cursor:
            cursor.execute(sql_query, params)
