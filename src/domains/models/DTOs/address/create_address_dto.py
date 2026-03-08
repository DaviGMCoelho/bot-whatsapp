from dataclasses import dataclass
from src.domains.models.DTOs.base_dto import BaseDTO

@dataclass
class CreateAddressRequestDTO(BaseDTO):
    active: str | bool
    code: str
    state: str
    city: str
    neighborhood: str
    street: str
    number: str
    postal_code: str
    complement: str
    company_id: int | str

    def __post_init__(self):
        self.active = self._translate_state(self.active)
        self._validate()

    def _validate(self):
        for field, field_type in self.__annotations__.items():
            value = getattr(self, field)
            if not isinstance(value, field_type):
                error = f'Campo "{field}" precisa ser {field_type}'
                raise TypeError(error)
