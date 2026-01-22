class Catalog:
    def __init__(self, code: str, name: str, company: str, active: bool = True):
        self.code = code
        self.name = name
        self.company = company
        self.active = active

        self._validate()

    def _validate(self):
        for arg, value in self.__dict__.items():
            if value is None:
                error = f'{arg} não pode ser None'
                raise ValueError(error)
