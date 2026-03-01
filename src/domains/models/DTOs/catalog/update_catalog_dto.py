class UpdateCatalogDTO:
    def __init__(self, code: str, company: str, name: str = None, active: str = None):
        self.code = code
        self.company = company
        self.name = name
        self.active = active

        self._validate()

    def to_dict(self):
        data = {}

        if self.name is not None:
            data['name'] = self.name.strip()
        if self.active is not None:
            data['active'] = self.active.lower() == 'true'

        return data


    def _validate(self):
        if not isinstance(self.code, str) or not self.code.strip():
            raise ValueError("Código não pode ser vazio")
        if self.name:
            if not isinstance(self.name, str) or not self.name.strip():
                raise ValueError('Nome não pode ser vazio ou apenas espaços')
        if self.company:
            if not isinstance(self.company, str) or not self.company.strip():
                raise ValueError('Empresa não pode ser vazio ou apenas espaços')
        if self.active:
            self._validate_active(self.active)


    def _validate_active(self, active: str):
        if active and active.strip().lower() not in ("on", "off"):
            raise ValueError('Active inválido, apenas "on" ou "off"')
