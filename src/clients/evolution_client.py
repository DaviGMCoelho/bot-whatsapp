import os

import requests

class EvolutionClient:
    def __init__(self, api_key: str, host: str):
        self.base_url = f'http://{host}:8080'
        self.headers = {
            "apikey": api_key,
            "Content-Type": "application/json"
        }

    def send_message(self, instance, sender_number, message):
        url = f"{self.base_url}/message/sendText/{instance}"

        payload = {
            "number": sender_number,
            "text": message,
            "delay": 123
        }
        response = requests.request("POST", url, json=payload, headers=self.headers, timeout=(3, 30))
        return response
