from dataclasses import dataclass
from src.domains.models.DTOs.base_dto import BaseDTO

@dataclass
class ChangeAddressStateRequestDTO(BaseDTO):
    company_id: int
    address_code: str
    active: str | bool

    def __post__init__(self):
        self.active = self._translate_state(self.active)
