from src.services.webhook_service import WebhookService

class WebhookController:
    def __init__(self, webhook_service: WebhookService):
        self.webhook = webhook_service

    def handle_webhook(self, data):
        messages = data.get('messages') if data else []
        if not messages:
            return {'status': 'ok', 'message': 'no messages to process'}
        return self.webhook.process_messages(messages)
