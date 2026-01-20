class CreateItemDTO:
    def __init__(self, code: str, name: str, description: str, price: str, catalog: str, active: str):
        self.code = code
        self.name = name
        self.description = description
        self.price = price
        self.catalog = catalog
        self.active = active

        self._validate()

    def _validate(self):
        for arg, value in self.__dict__.items():
            if value is None or (isinstance(value, str) and not value.strip()):
                error = f'{arg} não pode ser vazia'
                raise ValueError(error)
        self._validate_price(self.price)
        self._validate_active(self.active)
        self._validate_catalog(self.catalog)

    def _validate_price(self, price: str):
        if not price.replace(".", "", 1).isdigit():
            raise ValueError("Preço inválido")
        if len(price.split(".")[1]) > 2 if "." in price else False:
            raise ValueError("Preço deve ter no máximo 2 casas decimais")

    def _validate_active(self, active: str):
        if active.lower() not in ("true", "false"):
            raise ValueError("Active inválido, apenas 'true' ou 'false'")

    def _validate_catalog(self, catalog_id: str):
        if not catalog_id.isdigit():
            raise ValueError('Catálogo inválido, deve ser um inteiro')
