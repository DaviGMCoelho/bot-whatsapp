from psycopg2.extensions import connection
from src.repositories.postgres.base_repository import PostgresBaseRepository
from src.domains.models.quote import Quote
class QuoteRepository(PostgresBaseRepository):
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
            return Quote(
                text = quote[0],
                company_id = quote[1],
                type = quote[2],
                code = quote[3]
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
