from decimal import Decimal

class UpdateItemDTO:
    def __init__(self, code: str, company: int, catalog: str, name: str = None, description: str = None, price: str = None):
        self.code = code.strip()
        self.company = company
        self.catalog = catalog.strip() 
        self.name = name.strip() if name else None
        self.description = description.strip() if description else None
        self.price = price.strip() if price else None


        self._validate()

    def to_dict(self):
        data = {}

        if self.name is not None:
            data['name'] = self.name.strip()
        if self.description is not None:
            data['description'] = self.description
        if self.price is not None:
            data['price'] = Decimal(self.price)

        return data


    def _validate(self):
        if not self.code or not isinstance(self.code, str) or not self.code.strip():
            if not isinstance(self.code, str) or not self.code.strip():
                raise ValueError("Código não pode ser vazio")
        if self.name:
            if not isinstance(self.name, str) or not self.name.strip():
                raise ValueError('Nome não pode ser vazio ou apenas espaços')
        if self.description:
            if not isinstance(self.description, str) or not self.description.strip():
                raise ValueError('Descrição não pode ser vazia ou apenas espaços')
        if self.price:
            self._validate_price(self.price)
        if self.catalog:
            self._validate_catalog(self.catalog)


    def _validate_price(self, price: str):
        price_clean = price.strip()
        if not price_clean:
            raise ValueError('Preço não pode ser vazio')
        parts = price_clean.split('.')
        if len(parts) > 2:
            raise ValueError("Preço inválido: formato numérico incorreto")
        if not parts[0].isdigit() or (len(parts) == 2 and not parts[1].isdigit()):
            raise ValueError("Preço inválido: Deve conter apenas números")
        if len(parts) == 2 and len(parts[1]) > 2:
            raise ValueError('Preço deve ter no máximo 2 casas decimais')

    def _validate_active(self, active: str):
        if active and active.strip().lower() not in ("on", "off"):
            raise ValueError('Active inválido, apenas "on" ou "off"')

    def _validate_catalog(self, catalog_id: str):
        if catalog_id and not catalog_id.strip().isdigit():
            raise ValueError('Catálogo inválido, deve ser um inteiro')
