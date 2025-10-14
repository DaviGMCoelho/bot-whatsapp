from src.models.contact import Contact
from src.services.evolution_service import EvolutionService


class WebhookService:
    def __init__(self):
        self.evolution = EvolutionService()

    def process_messages(self, messages):
        for message in messages:
            if message['key']['fromMe'] is False:
                sender = Contact('Nome', message['key']['remoteJid'].split('@')[0])
                text = message['message'].get('conversation') or \
                    message['message'].get('extendedTextMessage', {}).get('text', '')

                response_text = f'Recebi sua mensagem: {text}'
                self.evolution.send_message(sender, response_text)
        return {"status": "ok"}
