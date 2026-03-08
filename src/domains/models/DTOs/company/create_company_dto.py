class CreateCompanyDTO:
    def __init__(self, name: str, cnpj: str, operation: dict):
        if not name:
            raise ValueError('Nome é obrigatório')
        if operation is not None and not isinstance(operation, dict):
            raise ValueError('Operation deve ser um dicionário')

        self.name = name
        self.cnpj = cnpj
        self.operation = operation or {}
