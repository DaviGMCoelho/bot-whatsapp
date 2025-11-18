from src.repositories.postgres.base_repository import PostgresBaseRepository

class MessageRepository (PostgresBaseRepository):
    def message_history(self, remoteJid: str, instance: str):
        connection, cursor = self._connection.get_connection()
        sql_query = self._load_query(r'data\sql_queries\message_history.sql')
        with connection:
            cursor.execute(sql_query, {'instance': instance, 'remoteJid': remoteJid})
        messages = cursor.fetchall()
        message_history = [
            {
                'role': role,
                'content': content
            }
            for role, content in messages
        ]
        return message_history
