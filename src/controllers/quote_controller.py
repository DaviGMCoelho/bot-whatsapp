from src.services.quote_service import QuoteService
from src.domains.models.DTOs.quotes.create_quote_dto import CreateQuoteRequestDTO
from src.domains.models.DTOs.quotes.change_quote_state_dto import ChangeStateQuoteRequestDTO
class QuoteController:
    def __init__(self, service: QuoteService):
        self.service = service

    def add(self, request: dict):
        company_id = int(request.get('company_id'))
        quote = CreateQuoteRequestDTO(
            quote = request.get('quote_text'),
            company_id = company_id,
            quote_type = request.get('quote_type'),
            active = request.get('active'),
            code = request.get('code')
        )
        return self.service.add_quote(quote)
    
    def change_state(self, request: dict):
        company_id = int(request.get('company_id'))
        code = request.get('quote_code')
        active = request.get('active')
        change_state = ChangeStateQuoteRequestDTO(
            company = company_id,
            code = code,
            active = active
        )
        return self.service.change_state(change_state)
