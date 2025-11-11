import requests

class EvolutionAPI:
    def __init__(self, api_key: str):
        self.headers = {
            "apikey": api_key,
            "Content-Type": "application/json"
        }

    def send_message1(self, instance, sender_number, message):
        base_url = "localhost:8080"
        url = f"http://{base_url}/message/sendText/{instance}"

        payload = {
            "number": sender_number,
            "textMessage": { "text": message }
        }

        response = requests.request("POST", url, json=payload, headers=self.headers, timeout=(3, 30))
        return response
    
    def send_message(self, instance, sender_number, message):
        base_url = "localhost:8080"
        url = f"http://{base_url}/message/sendText/{instance}"

        payload = {
            "number": sender_number,
            "text": message,
            "delay": 123
        }

        response = requests.request("POST", url, json=payload, headers=self.headers, timeout=(3, 30))
        return response
