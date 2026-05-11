from src.services.base_service import BaseService
from src.database.connection_pg import PostgresConn
from src.repositories.postgres.quote.quote_repository import QuoteRepository
from src.repositories.chroma.quote_chroma_repo import QuoteChromaRepository
from src.domains.models.DTOs.quotes.create_quote_dto import CreateQuoteRequestDTO
from src.domains.models.DTOs.quotes.create_quote_chroma_dto import CreateChromaQuoteDTO
from src.domains.models.DTOs.quotes.change_quote_state_dto import ChangeStateQuoteRequestDTO
from src.domains.models.DTOs.quotes.update_quote_dto import UpdateQuoteRequestDTO
from src.domains.models.full_quote import FullQuote
class QuoteService(BaseService):
    def __init__(self, psql_conn: PostgresConn, psql_repo: QuoteRepository, chroma_repo: QuoteChromaRepository):
        self.psql_conn = psql_conn
        self.psql_repo = psql_repo
        self.chroma_repo = chroma_repo

    def _generate_quote_chroma_id(self, quote_id: int):
        return f'quote_{quote_id}'

    def _get_quote_type_id(self, conn, quote_type: str, company_id: int):
        return self.psql_repo.get_quote_type(conn, quote_type, company_id)
    
    def _built_create_chroma_quote(self, quote_id: str, full_quote: FullQuote):
        return CreateChromaQuoteDTO(
                quote_id = self._generate_quote_chroma_id(quote_id),
                quote = full_quote.text,
                company_id = full_quote.company_id,
                quote_type = full_quote.type,
                code = full_quote.code
            )

    def add_quote(self, dto: CreateQuoteRequestDTO):
        try:
            with self.psql_conn.transaction() as conn:
                type_id = self._get_quote_type_id(conn, dto.quote_type, dto.company_id)
                quote_id = self.psql_repo.insert_quote(conn, dto.quote, dto.code, dto.company_id, type_id, dto.active)
                chroma_quote = CreateChromaQuoteDTO(
                    quote_id = self._generate_quote_chroma_id(quote_id),
                    quote = dto.quote,
                    company_id = dto.company_id,
                    quote_type = dto.quote_type,
                    code = dto.code
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

    def change_state(self, dto: ChangeStateQuoteRequestDTO):
        try:
            with self.psql_conn.connect() as conn:
                company_id = dto.company
                code = dto.code
                quote_id = self.psql_repo.change_state(conn, code, company_id, dto.active)
                chroma_quote_id = self._generate_quote_chroma_id(quote_id)
                if not dto.active:
                    self.chroma_repo.delete_quote(chroma_quote_id)
                    self.chroma_repo.get_quote(chroma_quote_id, company_id)
                else:
                    quote = self.psql_repo.get_quote_by_code(conn, code, company_id)
                    quote_chroma = CreateChromaQuoteDTO(
                        quote_id = chroma_quote_id,
                        quote = quote.text,
                        company_id = quote.company_id,
                        quote_type = quote.quote_type,
                        code = quote.code
                    )
                    self.chroma_repo.upsert_quote(quote_chroma)
                    self.chroma_repo.get_quote(chroma_quote_id, company_id)
                return {
                    'status': 'sucess',
                    'message': 'Alteração de estado realizada corretamente'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'{__name__} - {str(e)}'
            }
        
    def update_quote(self, dto: UpdateQuoteRequestDTO):
        try:
            with self.psql_conn.connect() as conn:
                type_id = ''
                if dto.type:
                    type_id = self._get_quote_type_id(conn, dto.type, dto.company_id)
                data = dto.to_dict(type_id)
                quote_id = self.psql_repo.update_quote(conn, dto.company_id, dto.code, data)
                quote = self.psql_repo.get_quote_by_code(conn, dto.code, dto.company_id)
                chroma_quote = self._built_create_chroma_quote(quote_id, quote)
                self.chroma_repo.upsert_quote(chroma_quote)
            return {
                'status': 'sucess',
                'message': 'Alteração realiazda corretamente'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'{__name__} - {str(e)}'
            }

