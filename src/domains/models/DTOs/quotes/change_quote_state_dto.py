from dataclasses import dataclass

from src.domains.models.DTOs.base_dto import BaseDTO

@dataclass
class ChangeStateQuoteRequestDTO(BaseDTO):
    company: int
    code: str
    active: str | bool

    def __post_init__(self):
        self.active = self._translate_state(self.active)
        self._validate()

    def _validate(self):     
        if not isinstance(self.company, int):
            error = 'Campo "company" precisa ser inteiro'
            raise TypeError(error)
        if not isinstance(self.code, str):
            error = 'Campo "code" precisa ser string'
            raise TypeError(error)

        if self.company <= 0:
            error = 'Campo "company" precisa ser maior que zero'
            raise ValueError(error)
        for field in ("code", "company"):
            value = getattr(self, field)
            if not value:
                error = f'Campo "{field}" não pode ser vazio'
                raise ValueError(error)
