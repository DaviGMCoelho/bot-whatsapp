from src.services.message_service import MessageService

class MessageController:
    def __init__(self):
        self.service = MessageService()

    def process_data(self, instance: str, remote_jid: str, message: str):
        self.service.process_message(instance, remote_jid, message)
