from dataclasses import dataclass

@dataclass
class UpdateQuoteRequestDTO:
    code: str
    company_id: int
    text: str | None = None
    type: str | None = None

    def _validate(self):
        if not isinstance(self.code, str):
            raise ValueError('Código é obrigatório')
        if len(self.code) != 7:
            raise ValueError('Código precisa ser de 7 dígitos')
        if not isinstance(self.company_id, int):
            raise ValueError('Empresa é obrigatório')

    def to_dict(self, type_id: int = None):
        data = {}
        if isinstance(type_id, int):
            data['quote_type_id'] = type_id
        if isinstance(self.text, str):
            data['content'] = self.text
        return data

    def __post_init__(self):
        self._validate()
