from src.repositories.postgres.company.company_repository import CompanyRepository
from src.repositories.postgres.address.address_repository import AddressRepository
from src.database.connection_pg import PostgresConn
from src.models.company import Company
from src.models.address import Address

class CompanyService:
    def __init__(self, psql_conn: PostgresConn, company_repo: CompanyRepository, address_repo: AddressRepository):
        self.company_repo_psql = company_repo
        self.address_repo_psql = address_repo
        self.psql_conn = psql_conn

    def register_company(self, company: Company, address: Address):
        with self.psql_conn.transaction() as conn:
            company_id = self.company_repo_psql.company_data_register(conn, company)
            address.company_id = company_id
            self.address_repo_psql.insert(conn, address)
