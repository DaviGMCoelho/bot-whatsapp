class Memory:
    def __init__(self,
                 customer_id: int,
                 company_id: int,
                 memory_type: str,
                 content: str
                ):
        self.customer_id = customer_id
        self.company_id = company_id
        self.memory_type = memory_type
        self.content = content

        self._validate()

    def _validate(self):
        for arg, value in self.__dict__.items():
            if value is None:
                error = f'{arg} não pode ser vazio'
                return error
            if isinstance(value, int):
                if value <= 0:
                    error = f'{arg} não pode ser menor ou igual a zero'
                    raise ValueError(error)
            if isinstance(value, str):
                if not value.strip():
                    error = f'{arg} não pode estar em branco'
                    raise ValueError(error)

if __name__ == '__main__':
    memory = Memory(1, 'qqlrcoisa', 2, 'dadadadadaa')
