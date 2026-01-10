from src.services.item_service import ItemService
from src.domains.models.DTOs.create_item_dto import CreateItemDTO

class ItemController:
    def __init__(self, service: ItemService):
        self.service = service

    def register_item(self, request_raw: dict):
        item_dto = CreateItemDTO(
            request_raw['name'],
            request_raw['description'],
            request_raw['price'],
            request_raw['catalog'],
            request_raw['active']
        )
        register = self.service.register_item(item_dto)
        return register
