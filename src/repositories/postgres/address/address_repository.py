
from psycopg2.extensions import connection
from src.repositories.postgres.base_repository import PostgresBaseRepository
from src.domains.models.address import Address

class AddressRepository(PostgresBaseRepository):
    def __init__(self):
        super().__init__()
        self.ALLOWED_FIELDS = {'state', 'city', 'neighborhood', 'street', 'number',
                               'postal_code', 'complement', 'label'}

    def insert(self, conn: connection, address: Address):
        sql_query = self._load_query('address/queries/register_address.sql')

        with conn.cursor() as cursor:
            cursor.execute(sql_query, {
                'active': address.active,
                'code': address.code,
                'state': address.state, 
                'city': address.city,
                'neighborhood': address.neighborhood,
                'street': address.street,
                'number': address.number,
                'postal_code': address.postal_code,
                'complement': address.complement,
                'company_id': address.company_id
            })


    def update(self, conn: connection, company_id: int, code: str, data: dict):
        update_query_raw = self._load_query('address/queries/update_address.sql')
        update_query, params = self._build_update_query(
            update_query_raw, 
            self.ALLOWED_FIELDS,
            data = data
        )
        params['code'] = code
        params['company_id'] = company_id

        with conn.cursor() as cursor:
            cursor.execute(update_query, params)

    def change_state(self, conn: connection, company_id: int, active: str, address_code: str):
        sql_query = self._load_query('address/queries/change_address_state.sql')
        with conn.cursor() as cursor:
            cursor.execute (sql_query, {
                'active': active,
                'company_id': company_id,
                'address_code': address_code
                })

    def get_address_by_company_id(self, conn: connection, company_id: int):
        sql_query = self._load_query('address/queries/get_address_by_company_id.sql')
        with conn.cursor() as cursor:
            cursor.execute (sql_query, {
                'company_id': company_id
            })
            data = cursor.fetchone()
            return Address(
                active = data[1],
                code = data[2],
                state = data[3],
                city = data[4],
                neighborhood = data[5],
                street = data[6],
                number = data[7],
                postal_code = data[8],
                complement = data[9],
                label = data[10],
                company_id = company_id
            )
