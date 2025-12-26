from psycopg2.extensions import connection
from src.repositories.postgres.base_repository import PostgresBaseRepository
from src.models.company import Company


class CompanyRepository (PostgresBaseRepository):
    def company_data_register(self, conn: connection, company: Company):
        sql_query = self._load_query('company/queries/register_company.sql')
        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'name': company.name,
                'operation': company.opertation
                })
            return cursor.fetchone()[0]
