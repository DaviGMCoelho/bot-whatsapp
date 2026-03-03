from decimal import Decimal

from src.services.base_service import BaseService
from src.repositories.postgres.item.item_repository import ItemRepository
from src.repositories.postgres.company.company_repository import CompanyRepository
from src.repositories.postgres.catalog.catalog_repository import CatalogRepository
from src.database.connection_pg import PostgresConn
from src.domains.models.DTOs.item.create_item_dto import CreateItemDTO
from src.domains.models.DTOs.item.update_item_dto import UpdateItemDTO
from src.domains.models.DTOs.item.change_state_item_dto import ChangeStateItemRequestDTO

from src.domains.models.item import Item

class ItemService(BaseService):
    def __init__ (self, psql_conn: PostgresConn, company_repo: CompanyRepository, catalog_repo: CatalogRepository, item_repo: ItemRepository):
        self.catalog_repo_psql = catalog_repo
        self.company_repo_psql = company_repo
        self.item_repo_psql = item_repo
        self.psql_conn = psql_conn

    def _convert_to_item_model(self, create_item_dto: CreateItemDTO):
        code = create_item_dto.code
        name = create_item_dto.name
        description = create_item_dto.description
        price = Decimal(create_item_dto.price)
        catalog_id = int(create_item_dto.catalog)
        active = create_item_dto.active.lower() == "true"

        item = Item(
            code = code,
            name = name,
            description = description,
            price = price,
            catalog = catalog_id,
            active = active
        )
        return item

    def register_item(self, create_item_dto: CreateItemDTO):
        try:
            with self.psql_conn.connect() as conn:
                item = Item(
                    company = create_item_dto.company,
                    code = create_item_dto.code,
                    name = create_item_dto.name,
                    description = create_item_dto.description,
                    price = Decimal(create_item_dto.price),
                    catalog = self.catalog_repo_psql.get_catalog_by_code(conn, create_item_dto.catalog, create_item_dto.company)[0],
                    active = create_item_dto.active
                )
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

    def update_item(self, update_item_dto: UpdateItemDTO):
        try:
            with self.psql_conn.connect() as conn:
                catalog_id = self.catalog_repo_psql.get_catalog_by_code(conn, update_item_dto.catalog, update_item_dto.company)[0]
                update_item_dto.catalog = catalog_id
                self.item_repo_psql.update(conn, update_item_dto)

            return {
                'status': 'success',
                'message': 'Item atualizado corretamente'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'{__name__} - {str(e)}'
            }

    def change_item_state(self, change_state_item_dto: ChangeStateItemRequestDTO):
        with self.psql_conn.connect() as conn:
            catalog_id = self.catalog_repo_psql.get_catalog_by_code(conn, change_state_item_dto.catalog, change_state_item_dto.company)[0]
            self.item_repo_psql.change_state(conn, catalog_id, change_state_item_dto.company, change_state_item_dto.code, change_state_item_dto.active)
