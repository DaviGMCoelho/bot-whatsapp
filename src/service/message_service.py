import requests

class EvolutionAPI:
    def __init__(self): ...

    def send_message(self, instance, sender_number, message):
        base_url = "localhost"
        url = f"http://{base_url}:8080/message/sendText/{instance}"

        payload = {
            "number": sender_number,
            "textMessage": { "text": message }
        }

        headers = {
            "apikey": "YOUR_EVOLUTION_API_KEY",
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers, timeout=(3, 30))
        return response