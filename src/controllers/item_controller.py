from src.services.item_service import ItemService
from src.domains.models.DTOs.create_item_dto import CreateItemDTO
from src.domains.models.DTOs.update_item_dto import UpdateItemDTO

class ItemController:
    def __init__(self, service: ItemService):
        self.service = service

    def _organize_data(self, item_request: dict):
        item = {
            'code': item_request.get('code') or None,
            'name': item_request.get('name') or None,
            'description': item_request.get('description') or None,
            'price': item_request.get('price') or None,
            'catalog': item_request.get('catalog') or None,
            'active': item_request.get('active') or None
        }
        return item

    def register_item(self, request: dict):
        item = self._organize_data(request)
        create_item_dto = CreateItemDTO(
            code = item['code'],
            name = item['name'],
            description = item['description'],
            price = item['price'],
            catalog = item['catalog'],
            active = item['active']
        )
        register = self.service.register_item(create_item_dto)
        return register

    def update_item(self, request: dict):
        item = self._organize_data(request)
        update_item_dto = UpdateItemDTO(
            code = item['code'],
            name = item['name'],
            description = item['description'],
            price = item['price'],
            catalog = item['catalog'],
            active = item['active']
        )
        update = self.service.update_item(update_item_dto)
        return update