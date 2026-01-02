class CreateCompanyDTO:
    def __init__(self, name: str, operation: dict | None, address: dict | None):
        if not name:
            raise ValueError('Nome é obrigatório')
        if operation is not None and not isinstance(operation, dict):
            raise ValueError('Operation deve ser um dicionário')
        if address is not None and not isinstance(address, dict):
            raise ValueError('Address deve ser um dicionário')

        self.name = name
        self.operation = operation or {}
        self.address = address or {}
