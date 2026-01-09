class CreateCatalogDTO:
    def __init__(self, name: str, company: str, active: bool):
        if not name:
            raise ValueError('Nome é obrigatório')
        if company is not None and not isinstance(company, str):
            raise ValueError('Company deve ser um número')
        if active is not None and not isinstance(active, bool):
            raise ValueError('Active deve ser um booleano')

        self.name = name
        self.company = company
        self.active = active
