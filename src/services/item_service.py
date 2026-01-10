from decimal import Decimal

from src.repositories.postgres.item.item_repository import ItemRepository
from src.database.connection_pg import PostgresConn
from src.domains.models.DTOs.create_item_dto import CreateItemDTO
from src.domains.models.item import Item

class ItemService:
    def __init__ (self, psql_conn: PostgresConn, item_repo: ItemRepository):
        self.item_repo_psql = item_repo
        self.psql_conn = psql_conn

    def _convert_to_item_model(self, create_item_dto: CreateItemDTO):
        name = create_item_dto.name
        description = create_item_dto.description
        price = Decimal(create_item_dto.price)
        catalog_id = int(create_item_dto.catalog)
        active = create_item_dto.active.lower() == "true"

        item = Item(
            name = name,
            description = description,
            price = price,
            catalog = catalog_id,
            active = active
        )
        return item

    def register_item(self, create_item_dto: CreateItemDTO):
        try:
            item = self._convert_to_item_model(create_item_dto)
            with self.psql_conn.connect() as conn:
                self.item_repo_psql.insert(conn, item)

            return {
                'status': 'success',
                'message': 'Item registrado corretamente'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'{__name__} - {str(e)}'
            }
