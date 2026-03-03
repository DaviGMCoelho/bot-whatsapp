from src.services.item_service import ItemService
from src.domains.models.DTOs.item.create_item_dto import CreateItemDTO
from src.domains.models.DTOs.item.update_item_dto import UpdateItemDTO
from src.domains.models.DTOs.item.change_state_item_dto import ChangeStateItemRequestDTO
class ItemController:
    def __init__(self, service: ItemService):
        self.service = service

    def _organize_data(self, item_request: dict):
        item = {
            'company': item_request.get('company') or None,
            'code': item_request.get('code') or None,
            'name': item_request.get('name') or None,
            'description': item_request.get('description') or None,
            'price': item_request.get('price') or None,
            'catalog': item_request.get('catalog') or None,
            'active': item_request.get('active')
        }
        return item

    def register_item(self, request: dict):
        item = self._organize_data(request)
        create_item_dto = CreateItemDTO(
            company = item['company'],
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
            company = item['company'],
            code = item['code'],
            catalog = item['catalog'],
            name = item['name'],
            description = item['description'],
            price = item['price']
        )
        update = self.service.update_item(update_item_dto)
        return update
    
    def change_item_state(self, request: dict):
        item = self._organize_data(request)
        change_state = ChangeStateItemRequestDTO(
            company = item['company'],
            code = item['code'],
            catalog = item['catalog'],
            active = item['active']
        )
        change = self.service.change_item_state(change_state)
        return change
