from psycopg2.extensions import connection
from src.repositories.postgres.base_repository import PostgresBaseRepository

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

    def insert_quote(self, conn: connection, quote: str, company_id: int, quote_type_id: int, active: bool):
        sql_query = self._load_query('quote/queries/insert_quote.sql')
        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                "company_id": company_id,
                "quote_type_id": quote_type_id,
                "content": quote,
                "active": active
            })
            quote_id = cursor.fetchone()
            return quote_id[0]
