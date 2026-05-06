class Quote:
    def __init__(self, text: str, company_id: int, type: str, code: str):
        self.text = text
        self.company_id = company_id
        self.type = type
        self.code = code

    def _validate_code(self, code: str):
        return len(code) == 7

    def _validate(self):
        for arg, value in self.__dict__.items():
            if value is None:
                error = f'{arg} não pode ser None'
                raise ValueError(error)
        if not self._validate_code(self.code):
            raise ValueError('Code precisa ter 7 digitos')

    def __post_init__(self):
        self._validate()
