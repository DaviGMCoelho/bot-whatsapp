class CreateCatalogDTO:
    def __init__(self, code: str, name: str, company: str, active: str):
        self.code = code
        self.name = name
        self.company = company
        self.active = active

    def _validate(self):
        for arg, value in self.__dict__.items():
            if value is None or (isinstance(value, str) and not value.strip()):
                error = f'{arg} não pode ser vazia'
                raise ValueError(error)
        self._validate_company(self.company)
        self._validate_active(self.active)

    def _validate_active(self, active: str):
        if active.lower() not in ("true", "false"):
            raise ValueError("Active inválido, apenas 'true' ou 'false'")

    def _validate_company(self, company_id: str):
        if not company_id.isdigit():
            raise ValueError('Empresa inválida, deve ser um inteiro')