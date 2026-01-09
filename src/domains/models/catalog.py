class Catalog:
    def __init__(self, name: str, company: str, active: bool = True):
        self.name = name
        self.company = company
        self.active = active

    def _validate(self):
        for arg, value in self.__dict__.items():
            if value is None:
                error = f'{arg} não pode ser None'
                raise ValueError(error)
