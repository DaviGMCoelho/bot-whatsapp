from src.services.base_service import BaseService
from src.database.connection_pg import PostgresConn
from src.repositories.postgres.quote.quote_repository import QuoteRepository
from src.domains.models.DTOs.quotes.create_quote_dto import CreateQuoteRequestDTO

class QuoteService(BaseService):
    def __init__(self, psql_conn: PostgresConn, psql_repo: QuoteRepository):
        self.psql_conn = psql_conn
        self.psql_repo = psql_repo

    def _get_quote_type_id(self, conn, quote_type: str, company_id: int):
        return self.psql_repo.get_quote_type(conn, quote_type, company_id)

    def add_quote(self, dto: CreateQuoteRequestDTO):
        with self.psql_conn.transaction() as conn:
            type_id = self._get_quote_type_id(conn, dto.quote_type, dto.company_id)
            self.psql_repo.insert_quote(conn, dto.quote, dto.company_id, type_id, dto.active)
