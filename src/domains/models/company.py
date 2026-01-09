from src.domains.value_objects.operation import Operation

class Company:
    def __init__(self, name: str, operation: Operation, cnpj: str):
        if not name or not operation:
            raise ValueError('Nome da empresa é obrigatório')
        if not len(cnpj) == 14 or not isinstance(cnpj, str):
            raise ValueError('CNPJ inválido')

        self.name = name
        self.operation = operation
        self.active = False
        self.cnpj = cnpj

    def to_dict(self):
        return self.__dict__

    def activate(self):
        if not self.operation.has_open_day():
            raise ValueError('Empresa não pode ser ativada sem horário de funcionamento')
        self.active = True
