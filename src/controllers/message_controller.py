from src.services.message_service import MessageService

class MessageController:
    def __init__(self):
        self.service = MessageService()

    def process_data(self, instance: str, remote_jid: str, message: str):
        self.service.process_message(instance, remote_jid, message)

    def get_message_type(self, message_data: dict):
        msg_type = message_data.get('messageType')
        if msg_type == 'conversation' or 'conversation' in message_data:
            m_type = message_data.get('conversation')
        elif msg_type == 'extendedTextMessage' or 'extendedTextMessage' in message_data:
            m_type = message_data.get('extendedTextMessage').get('text')
        else:
            m_type = f'Tipo não reconhecido: {msg_type}'

        return str(m_type)
