from decimal import Decimal

class Item:
    def __init__(self,
                 company: str = None,
                 code: str = None,
                 name: str = None,
                 description: str = None,
                 price: Decimal = None,
                 catalog: int = None,
                 active: bool = None
                 ):
        self.company = company
        self.code = code
        self.name = name
        self.description = description
        self.price = price
        self.catalog = catalog
        self.active = active

        self._validate()

    def _validate(self):
        for arg, value in self.__dict__.items():
            if value is None:
                error = f'{arg} não pode ser None'
                raise ValueError(error)
        if not self._price_is_more_than_zero(self.price):
            raise ValueError('Preço precisa ser maior que zero!')

    def _price_is_more_than_zero(self, price: Decimal):
        return price > 0.0
