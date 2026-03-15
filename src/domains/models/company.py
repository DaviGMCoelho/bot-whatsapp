from src.domains.value_objects.operation import Operation

class Company:
    def __init__(self, name: str, operation: Operation, active: bool, cnpj: str):
        if not name or not operation:
            raise ValueError('Nome da empresa é obrigatório')
        if not len(cnpj) == 14 or not isinstance(cnpj, str):
            raise ValueError('CNPJ inválido')

        self.name = name
        self.operation = operation
        self.active = active
        self.cnpj = cnpj
