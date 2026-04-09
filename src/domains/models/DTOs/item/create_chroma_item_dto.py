from dataclasses import dataclass

@dataclass
class CreateChromaItemDTO:
    item_id: int
    code: str
    name: str
    description: str
    catalog_name: str
    company_id: int
    company_name: str

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'catalog_name': self.catalog_name,
        }
