from src.clients.evolution_client import EvolutionClient

class EvolutionService:
    def __init__(self, api_key: str):
        self.client = EvolutionClient(api_key)
        self.headers = {
            "apikey": api_key,
            "Content-Type": "application/json"
        }

    def send_message(self, instance, sender_number, message):
        self.client.send_message(instance, sender_number, message)