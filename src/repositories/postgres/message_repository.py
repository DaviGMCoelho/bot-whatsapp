from src.repositories.postgres.base_repository import PostgresBaseRepository

class MessageRepository (PostgresBaseRepository):
    def message_history(self, remoteJid: str, instance: str):
        sql_query = self._load_query("data/database/sql_queries/conversation_history.sql")

        with self.get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(sql_query, {'instance': instance, 'remoteJid': remoteJid})
                messages = cursor.fetchall()
                message_history = [
                    {
                        'role': 'bot' if role == 'true' else 'client',
                        'content': content
                    }
                    for role, content in messages
                ]
                return message_history
