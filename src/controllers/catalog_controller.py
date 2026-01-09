from src.services.catalog_service import CatalogService
from src.domains.models.DTOs.create_catalog_dto import CreateCatalogDTO

class CatalogController:
    def __init__(self, service: CatalogService):
        self.service = service

    def register_catalog(self, request_raw: dict):
        catalog_dto = CreateCatalogDTO(
            request_raw['name'],
            request_raw['company'],
            request_raw['active']
            )
        register = self.service.register_catalog(catalog_dto)
        return register
