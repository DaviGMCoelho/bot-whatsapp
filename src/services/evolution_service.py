import base64

from src.utils.http_client import HttpClient
from src.models.contact import Contact

class EvolutionService:
    def __init__(self):
        self.http_client = HttpClient(
            base_url='http://evolution-api:8080',
            headers= {"apikey": "1234", "Content-Type": "application/json"}
        )

    def send_message(self, contact: Contact, message: str):
        payload = {
            "number": contact.phone_number, 
            "textMessage": {
                "text": message
                }
            }
        self.http_client.post(r'/message/sendText/seller-bot', payload)

    def send_image(self, contact: Contact, image_path: str, caption:str = None):
        with open(image_path, 'rb') as image:
            image_b64 = base64.b64encode(image.read()).decode('utf-8')
        payload = {
            "number": contact.phone_number, 
            "mediaMessage": {
                "mediatype": "image",
                "fileName": "img.png",
                "caption": caption,
                "media": image_b64
                }
            }
        self.http_client.post(r'/message/sendmedia/seller-bot', payload)
