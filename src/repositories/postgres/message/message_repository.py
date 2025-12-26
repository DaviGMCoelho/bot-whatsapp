from psycopg2.extensions import connection
from src.repositories.postgres.base_repository import PostgresBaseRepository

class MessageRepository (PostgresBaseRepository):
    def message_history(self, conn: connection, remote_jid: str, instance: str):
        sql_query = self._load_query('message/queries/conversation_history.sql')

        with conn.cursor() as cursor:
            cursor.execute(sql_query, {'instance': instance, 'remoteJid': remote_jid})
            messages = cursor.fetchall()
            message_history = [
                {
                    'role': 'bot' if role == 'true' else 'client',
                    'content': content
                }
                for role, content in messages
            ]
            return message_history
