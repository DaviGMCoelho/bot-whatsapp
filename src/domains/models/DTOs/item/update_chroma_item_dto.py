from dataclasses import dataclass

@dataclass
class UpdateChromaItemDTO:
    product_id: str
    code: str
    company_id: str
    name: str = None
    description: str = None
    catalog_name: str = None
    company: str = None

    def __post_init__(self):
        self._validate()

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'catalog_name': self.catalog_name
        }

    def _validate(self):
        if not self.product_id or not isinstance(self.product_id, str):
            raise ValueError('Id precisa ser uma string')
        if not self.code or not isinstance(self.code, str):
            raise ValueError('Code precisa ser uma string')
        if not self.company:
            raise ValueError('Item precisa estar ligado a uma empresa')
        if not (self.name or self.description or self.catalog_name):
            raise ValueError('Pelo menos um dos campos precisa estar preenchido')
