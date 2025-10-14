import requests

class HttpClient:
    def __init__(self, base_url: str, headers: dict = None):
        self.base_url = base_url
        self.headers = headers or {}

    def post(self, endpoint: str, payload: dict):
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json() if response.ok else {"error": response.text}
