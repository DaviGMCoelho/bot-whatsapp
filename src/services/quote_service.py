from src.services.base_service import BaseService
from src.database.connection_pg import PostgresConn
from src.repositories.postgres.quote.quote_repository import QuoteRepository
from src.repositories.chroma.quote_chroma_repo import QuoteChromaRepository
from src.domains.models.DTOs.quotes.create_quote_dto import CreateQuoteRequestDTO
from src.domains.models.DTOs.quotes.create_quote_chroma_dto import CreateChromaQuoteDTO
class QuoteService(BaseService):
    def __init__(self, psql_conn: PostgresConn, psql_repo: QuoteRepository, chroma_repo: QuoteChromaRepository):
        self.psql_conn = psql_conn
        self.psql_repo = psql_repo
        self.chroma_repo = chroma_repo

    def _generate_quote_chroma_id(self, quote_id: int):
        return f'quote_{quote_id}'

    def _get_quote_type_id(self, conn, quote_type: str, company_id: int):
        return self.psql_repo.get_quote_type(conn, quote_type, company_id)

    def add_quote(self, dto: CreateQuoteRequestDTO):
        try:
            print('add service')
            with self.psql_conn.transaction() as conn:
                type_id = self._get_quote_type_id(conn, dto.quote_type, dto.company_id)
                quote_id = self.psql_repo.insert_quote(conn, dto.quote, dto.company_id, type_id, dto.active)
                chroma_quote = CreateChromaQuoteDTO(
                    quote_id = self._generate_quote_chroma_id(quote_id),
                    quote = dto.quote,
                    company_id = dto.company_id,
                    quote_type = dto.quote_type
                )
                self.chroma_repo.upsert_quote(chroma_quote)
            return {
                'status': 'sucess',
                'message': 'Quote registrado corretamente'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'{__name__} - {str(e)}'
            }
