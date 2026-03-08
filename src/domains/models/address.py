class Address:
    def __init__(self,
                 active: bool,
                 code: str,
                 state: str,
                 city: str,
                 neighborhood: str,
                 street: str,
                 number: str,
                 postal_code: str,
                 complement: str,
                 label: str = '' ,
                 company_id: str = ''
                 ):
        self.active = active
        self.code = code
        self.state = state
        self.city = city
        self.neighborhood = neighborhood
        self.street = street
        self.number = number
        self.postal_code = postal_code
        self.complement = complement
        self.label = label
        self.company_id = company_id

        self._validate()

    def _validate(self):
        for arg, value in self.__dict__.items():
            if value is None:
                error = f'{arg} não pode ser None'
                raise ValueError(error)
        if not self._is_valid_postal_code(self.postal_code):
            raise ValueError('CEP inválido')

    def _is_valid_postal_code(self, postal_code: str):
        return len(postal_code) == 8 and postal_code.isdigit()
