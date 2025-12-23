from src.repositories.postgres.base_repository import PostgresBaseRepository

class PostgreManagerRepository (PostgresBaseRepository):
    def init_database(self):
        try:
            sql_query = self._load_query("data/database/db_setup/create_tables.sql")
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql_query)
                return 200
        
        except Exception as e:
            print('Erro ao criar tabelas', e)
            return e, 'error'
