from psycopg2.extensions import connection
from src.repositories.postgres.base_repository import PostgresBaseRepository
from src.domains.models.company import Company

class CompanyRepository (PostgresBaseRepository):
    def __init__(self):
        super().__init__()
        self.ALLOWED_FIELDS = {'name', 'active', 'operation'}

    def insert(self, conn: connection, company: Company):
        sql_query = self._load_query('company/queries/register_company.sql')
        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'name': company.name,
                'operation': company.operation.to_json()
                })
            return cursor.fetchone()[0]

    def update(self, conn: connection, cnpj: str, data: dict):
        query_raw = self._load_query('company/queries/update_company.sql')
        sql_query, params = self._build_update_query(query_raw, self.ALLOWED_FIELDS, data)
        params['cnpj'] = cnpj

        with conn.cursor() as cursor:
            cursor.execute(sql_query, params)

    def change_state(self, conn: connection, company_id: int, active: bool):
        sql_query = self._load_query('company/queries/change_company_state.sql')
        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'active': active,
                'company_id': company_id
            })

    def get_company_operation(self, conn: connection, cnpj: str):
        sql_query = self._load_query('company/queries/get_company_operation.sql')
        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'cnpj': cnpj
            })
            return cursor.fetchone()[0]

    def get_company_by_cnpj(self, conn: connection, company_cnpj: str):
        sql_query = self._load_query('company/queries/get_company_by_cnpj.sql')
        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                "cnpj": company_cnpj
            })
            return cursor.fetchone()
