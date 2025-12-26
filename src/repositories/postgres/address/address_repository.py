from psycopg2.extensions import connection
from src.repositories.postgres.base_repository import PostgresBaseRepository
from src.models.address import Address

class AddressRepository(PostgresBaseRepository):
    def insert(self, conn: connection, address: Address):
            sql_query = self._load_query('address/queries/register_address.sql')

            with conn.cursor() as cursor:
                cursor.execute(sql_query, {
                    'state': address.state, 
                    'city': address.city,
                    'neighrborhood': address.neighborhood,
                    'street': address.street,
                    'number': address.number,
                    'postal_code': address.postal_code,
                    'complement': address.complement,
                    'label': address.label,
                    'company': address.company
                })