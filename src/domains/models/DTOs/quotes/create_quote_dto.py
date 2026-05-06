from dataclasses import dataclass
from src.domains.models.DTOs.base_dto import BaseDTO

@dataclass
class CreateQuoteRequestDTO(BaseDTO):
    quote: str
    company_id: int
    quote_type: str
    active: bool
    code: str

    def __post_init__(self):
        self.active = self._translate_state(self.active)

