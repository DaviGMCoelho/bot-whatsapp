from psycopg2.extensions import connection
from src.repositories.postgres.base_repository import PostgresBaseRepository

from src.domains.models.DTOs.item.update_item_dto import UpdateItemDTO

from src.domains.models.item import Item
from src.domains.models.full_item import FullItem

class ItemRepository(PostgresBaseRepository):
    def __init__(self):
        super().__init__()
        self.ALLOWED_FIELDS = {'name', 'description', 'price', 'catalog_id', 'active'}

    def insert(self, conn: connection, item: Item):
        sql_query = self._load_query('item/queries/register_item.sql')

        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'company_id': item.company_id,
                'code': item.code,
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'catalog_id': item.catalog,
                'active': item.active
            })
            item_id = cursor.fetchone()
            return item_id[0]


    def update(self, conn: connection, update_item_dto: UpdateItemDTO, catalog_id: int):
        query_raw = self._load_query('item/queries/update_item.sql')
        sql_query, params = self._build_update_query(query_raw, self.ALLOWED_FIELDS, update_item_dto.to_dict())
        params['code'] = update_item_dto.code
        params['company_id'] = update_item_dto.company
        params['catalog_id'] = catalog_id
        with conn.cursor() as cursor:
            cursor.execute(sql_query, params)
            item_id = cursor.fetchone()
            return item_id[0]

    def change_state(self, conn: connection, catalog_id: int, company_id: int, item_code: str, active: bool):
        sql_query = self._load_query('item/queries/change_item_state.sql')

        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'active': active,
                'code': item_code,
                'company_id': company_id,
                'catalog_id': catalog_id
            })
            item_id = cursor.fetchone()
            return item_id[0]

    def get_item_by_code(self, conn: connection, item_code: str, company_id: int):
        sql_query = self._load_query('item/queries/get_item_by_code.sql')
        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'item_code': item_code,
                'company_id': company_id
            })
            item = cursor.fetchone()
            return FullItem(
                item_id = item[0],
                company_id = item[1],
                company_name = item[2],
                code = item[3],
                name = item[4],
                description = item[5],
                price = item[6],
                catalog = item[7],
                catalog_name = item[8],
                active = item[9]
            )