import os

from src.services.evolution_service import EvolutionService
from src.services.gemini_service import GeminiService
from src.repositories.postgres.message_repository import MessageRepository
class MessageService:
    def __init__(self):
        self.evolution = EvolutionService(os.getenv("AUTHENTICATION_API_KEY"))
        self.gemini = GeminiService(os.getenv("GOOGLE_API_KEY"), r'data\base_dados.csv', 0)
        self.repository = MessageRepository()

    def process_message(self, instance, remote_jid, user_message):
        customer_info = ''
        history = ''
        conversation_history = self.repository.message_history(remote_jid, instance)

        if conversation_history:
            for message in conversation_history:
                history += f'{message['role']}: {message['content']}\n'

        response = self.gemini.generate_message(user_message, customer_info, history)

        sender_number = remote_jid.split('@')[0]
        self.evolution.send_message(instance, sender_number, response)
