from src.repositories.postgres.catalog.catalog_repository import CatalogRepository
from src.repositories.postgres.company.company_repository import CompanyRepository
from src.database.connection_pg import PostgresConn
from src.domains.models.DTOs.create_catalog_dto import CreateCatalogDTO
from src.domains.models.DTOs.update_catalog_dto import UpdateCatalogDTO
from src.domains.models.catalog import Catalog

class CatalogService:
    def __init__(self, psql_conn: PostgresConn, catalog_repo: CatalogRepository, company_repo: CompanyRepository):
        self.catalog_repo_psql = catalog_repo
        self.company_repo_psql = company_repo
        self.psql_conn = psql_conn

    def register_catalog(self, create_catalog_dto: CreateCatalogDTO):
        try:
            catalog = Catalog(
                create_catalog_dto.code,
                create_catalog_dto.name,
                create_catalog_dto.company,
                create_catalog_dto.active
                )
                
            with self.psql_conn.connect() as conn:
                catalog.company = self.company_repo_psql.get_company_by_cnpj(conn, create_catalog_dto.company)
                self.catalog_repo_psql.insert(conn, catalog)

            return {
                'status': 'success',
                'message': 'Catálogo registrado corretamente'
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f'{__name__} - {str(e)}'
            }

    def update_catalog(self, update_catalog_dto: UpdateCatalogDTO):
        try:
            catalog = update_catalog_dto.to_dict()
            with self.psql_conn.connect() as conn:
                self.catalog_repo_psql.update(conn, update_catalog_dto.code, catalog)
            return {
                'status': 'sucess',
                'message': 'Catalogo atualizado corretamente'
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': f'{__name__} - {str(e)}'
            }
