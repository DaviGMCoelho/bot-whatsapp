from decimal import Decimal
from src.domains.models.item import Item

class FullItem(Item):
    def __init__(
              self,
              item_id: int,
              company_id: int,
              company_name: str,
              code: str,
              name: str,
              description: str,
              price: Decimal,
              catalog: int,
              catalog_name: str,
              active: str
            ):
        super().__init__(item_id, company_id, code, name, description, price, catalog, active)
        self.company_name = company_name
        self.catalog_name = catalog_name
