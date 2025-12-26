from src.clients.evolution_client import EvolutionClient

class EvolutionService:
    def __init__(self, client: EvolutionClient):
        self.client = client

    def send_message(self, instance, sender_number, message):
        self.client.send_message(instance, sender_number, message)
