from psycopg2.extensions import connection
from src.repositories.postgres.base_repository import PostgresBaseRepository
from src.domains.models.quote import Quote
from src.domains.models.full_quote import FullQuote
class QuoteRepository(PostgresBaseRepository):
    def __init__(self):
        super().__init__()
        self.allowed_fields = {'content', 'quote_type_id'}

    def get_quote_type(self, conn: connection, quote_type: str, company_id: int):
        sql_query = self._load_query('quote/queries/get_quote_type_id.sql')
        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'quote_type': quote_type,
                'company_id': company_id
            })
            type_id = cursor.fetchone()
            return type_id[0]

    def get_quote_by_code(self, conn: connection, quote_code: str, company_id: int):
        sql_query = self._load_query('quote/queries/get_quote_by_code.sql')
        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'code': quote_code,
                'company_id': company_id
            })
            quote = cursor.fetchone()
            return FullQuote(
                text = quote[0],
                company_id = quote[1],
                type_id = quote[2],
                quote_type = quote[3],
                code = quote[4]
            )

    def insert_quote(self, conn: connection, quote: str, quote_code: str, company_id: int, quote_type_id: int, active: bool):
        sql_query = self._load_query('quote/queries/insert_quote.sql')
        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                "company_id": company_id,
                "code": quote_code,
                "quote_type_id": quote_type_id,
                "content": quote,
                "active": active
            })
            quote_id = cursor.fetchone()
            return quote_id[0]

    def change_state(self, conn: connection, code: str, company_id: int, active: bool):
        sql_query = self._load_query('quote/queries/change_state.sql')
        with conn.cursor() as cursor:
            cursor.execute(sql_query, 
                {
                    'active': active,
                    'code': code,
                    'company_id': company_id
                })
            quote_id = cursor.fetchone()
            return quote_id[0]

    def update_quote(self, conn: connection, company_id: int, quote_code: str, data: dict):
        query_raw = self._load_query('quote/queries/update_quote.sql')
        sql_query, params = self._build_update_query(query_raw, self.allowed_fields, data)
        params['company_id'] = company_id
        params['quote_code'] = quote_code
        with conn.cursor() as cursor:
            cursor.execute(sql_query, params)
            quote_id = cursor.fetchone()
            return quote_id
