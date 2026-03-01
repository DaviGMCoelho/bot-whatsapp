class UpdateCompanyDTO:
    def __init__(self,
        cnpj: str,
        name: str = None,
        active: str = None,
        operation: dict = None,
        address: dict = None
    ):
        self.cnpj = cnpj.strip()
        self.name = name
        self.active = active
        self.operation = operation
        self.address = address

    def to_base_dict(self):
        data = {}
        if self.name is not None:
            data['name'] = self.name.strip()
        if self.active is not None:
            data['active'] = self.active.strip()
        return data

    def to_operation_dict(self):
        data = {}
        if self.operation is None:
            raise ValueError('Operação não pode estar vazia para atualizar!')
        return {'operation': self.operation}

    def to_address_dict(self):
        data = {}
        if self.address is None:
            raise ValueError('Endereço não pode estar vazio para atualizar!')
        return self.address
