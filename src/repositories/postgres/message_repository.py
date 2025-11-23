from src.repositories.postgres.base_repository import PostgresBaseRepository

class MessageRepository (PostgresBaseRepository):
    def message_history(self, remoteJid: str, instance: str):
        connection, cursor = self._connection
        sql_query = self._load_query(r'data\database\sql_queries\conversation_history.sql')

        with connection:
            cursor.execute(sql_query, {'instance': instance, 'remoteJid': remoteJid})
        messages = cursor.fetchall()
        message_history = [
            {
                'role': 'cliente' if role == 'true' else 'bot',
                'content': content
            }
            for role, content in messages
        ]
        return message_history
