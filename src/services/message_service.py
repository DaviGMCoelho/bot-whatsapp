import os
from dotenv import load_dotenv
from src.database.connection_pg import PostgresConn
from src.services.evolution_service import EvolutionService
from src.services.gemini_service import GeminiService
from src.repositories.postgres.message.message_repository import MessageRepository
class MessageService:
    def __init__(self,
                 psql_conn: PostgresConn,
                 evolution_service: EvolutionService,
                 gemini_service: GeminiService,
                 repository: MessageRepository
                 ):
        self.psql_conn = psql_conn
        self.evolution = evolution_service
        self.gemini = gemini_service
        self.repository = repository

    def process_message(self, instance, remote_jid, user_message):
        customer_info = ''
        history = ''

        with self.psql_conn.connect() as conn:
            messages = self.repository.message_history(conn, remote_jid, instance)

        if messages:
            for message in messages:
                history += f'{message['role']}: {message['content']}\n'

        response = self.gemini.generate_message(user_message, customer_info, history)

        sender_number = remote_jid.split('@')[0]
        self.evolution.send_message(instance, sender_number, response)
