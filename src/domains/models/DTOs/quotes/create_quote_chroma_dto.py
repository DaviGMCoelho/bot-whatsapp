from dataclasses import dataclass
from src.domains.models.DTOs.base_dto import BaseDTO

@dataclass
class CreateChromaQuoteDTO(BaseDTO):
    quote_id: str
    quote: str
    company_id: int
    quote_type: str
    code: str

    def to_dict(self):
        return {
            'quote': self.quote,
            'quote_type': self.quote_type,
            'company_id': self.company_id
        }
