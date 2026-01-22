from src.services.catalog_service import CatalogService
from src.domains.models.DTOs.create_catalog_dto import CreateCatalogDTO
from src.domains.models.DTOs.update_catalog_dto import UpdateCatalogDTO

class CatalogController:
    def __init__(self, service: CatalogService):
        self.service = service

    def _organize_data(self, catalog_request: dict):
        catalog = {
            'code': catalog_request.get('code') or None,
            'name': catalog_request.get('name') or None,
            'company': catalog_request.get('company') or None,
            'active': catalog_request.get('active') or None
        }
        return catalog

    def register_catalog(self, request: dict):
        create_catalog_dto = CreateCatalogDTO(
            request['code'],
            request['name'],
            request['company'],
            request['active']
            )
        register = self.service.register_catalog(create_catalog_dto)
        return register

    def update_catalog(self, request: dict):
        catalog = self._organize_data(request)
        update_catalog_dto = UpdateCatalogDTO(
            code = catalog['code'],
            name = catalog['name'],
            active = catalog['active']
        )
        update = self.service.update_catalog(update_catalog_dto)
        return update
