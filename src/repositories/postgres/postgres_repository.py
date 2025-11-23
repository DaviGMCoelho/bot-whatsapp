from src.repositories.postgres.base_repository import PostgresBaseRepository

class PostgreManagerRepository (PostgresBaseRepository):
    def init_database(self):
        try:
            connection, cursor = self._connection
            sql_query = self._load_query(r'data\database\db_setup\create_tables.sql')

            with connection:
                cursor.execute(sql_query)

            return 200

        except Exception as e:
            print('Erro ao criar tabelas', e)
            return e, 'error'
