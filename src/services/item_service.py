from decimal import Decimal
from src.services.base_service import BaseService
from src.repositories.postgres.item.item_repository import ItemRepository
from src.repositories.chroma.product_chroma_repo import ProductChromaRepository
from src.repositories.postgres.company.company_repository import CompanyRepository
from src.repositories.postgres.catalog.catalog_repository import CatalogRepository
from src.database.connection_pg import PostgresConn
from src.domains.models.DTOs.item.create_item_dto import CreateItemDTO
from src.domains.models.DTOs.item.create_chroma_item_dto import CreateChromaItemDTO
from src.domains.models.DTOs.item.update_item_dto import UpdateItemDTO
from src.domains.models.DTOs.item.update_chroma_item_dto import UpdateChromaItemDTO
from src.domains.models.DTOs.item.change_state_item_dto import ChangeStateItemRequestDTO
from src.domains.models.full_item import FullItem

from src.domains.models.item import Item

class ItemService(BaseService):
    def __init__ (self, psql_conn: PostgresConn, company_repo: CompanyRepository, catalog_repo: CatalogRepository, item_repo: ItemRepository, item_chroma_repo: ProductChromaRepository):
        self.catalog_repo_psql = catalog_repo
        self.company_repo_psql = company_repo
        self.item_repo_psql = item_repo
        self.item_repo_chroma = item_chroma_repo
        self.psql_conn = psql_conn

    def _generate_product_chroma_id(self, product_id: int):
        return f'product_{product_id}'

    def _convert_to_item_model(self, create_item_dto: CreateItemDTO):
        company = create_item_dto.company
        code = create_item_dto.code
        name = create_item_dto.name
        description = create_item_dto.description
        price = Decimal(create_item_dto.price)
        catalog_id = int(create_item_dto.catalog)
        active = create_item_dto.active.lower() == "true"

        item = Item(
            company_id = company,
            code = code,
            name = name,
            description = description,
            price = price,
            catalog = catalog_id,
            active = active
        )
        return item
    
    def _build_chroma_update_item_dto(self, item: FullItem):
        product_id = self._generate_product_chroma_id(item.item_id)
        return UpdateChromaItemDTO(
            product_id = product_id,
            code = item.code,
            company_id = item.company_id,
            name = item.name,
            description = item.description,
            catalog_name = item.catalog_name,
            company = item.company_id
        )

    def register_item(self, create_item_dto: CreateItemDTO):
        try:
            with self.psql_conn.connect() as conn:
                catalog = self.catalog_repo_psql.get_catalog_by_code(conn, create_item_dto.catalog, create_item_dto.company)
                company = self.company_repo_psql.get_company_by_id(conn, create_item_dto.company)
                item = Item(
                    company_id = create_item_dto.company,
                    code = create_item_dto.code,
                    name = create_item_dto.name,
                    description = create_item_dto.description,
                    price = Decimal(create_item_dto.price),
                    catalog = catalog[0],
                    active = create_item_dto.active
                )
                item_id = self.item_repo_psql.insert(conn, item)
                item.item_id = item_id
                create_chroma_item = CreateChromaItemDTO(
                    item_id =  self._generate_product_chroma_id(item_id),
                    code = item.code,
                    name = item.name,
                    description = item.description,
                    catalog_name = catalog[2],
                    company_id = company[0],
                    company_name = company[1]
                )
                self.item_repo_chroma.upsert_product(create_chroma_item)

            return {
                'status': 'success',
                'message': 'Item registrado corretamente'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'{__name__} - {str(e)}'
            }

    def update_item(self, dto: UpdateItemDTO):
        try:
            with self.psql_conn.connect() as conn:
                catalog = self.catalog_repo_psql.get_catalog_by_code(conn, dto.catalog, dto.company)
                self.item_repo_psql.update(conn, dto, catalog[0])
                full_item = self.item_repo_psql.get_item_by_code(conn, dto.code, dto.company)
                chroma_dto = self._build_chroma_update_item_dto(full_item)
                self.item_repo_chroma.update_product(chroma_dto)
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
            product_id = self.item_repo_psql.change_state(conn, catalog_id, change_state_item_dto.company, change_state_item_dto.code, change_state_item_dto.active)
            print(change_state_item_dto.active)
            if not change_state_item_dto.active:
                print(product_id)
                product = self._generate_product_chroma_id(product_id)
                print(product)
                self.item_repo_chroma.delete_product(product)
                print('produto deletado')
            else:
                product = self.item_repo_psql.get_item_by_code(conn, change_state_item_dto.code, change_state_item_dto.company)
                product_chroma = CreateChromaItemDTO(
                    item_id = self._generate_product_chroma_id(product.item_id),
                    code = product.code,
                    name = product.name,
                    description = product.description,
                    catalog_name = product.catalog_name,
                    company_id = change_state_item_dto.company,
                    company_name = product.company_name
                )
                self.item_repo_chroma.upsert_product(product_chroma)
