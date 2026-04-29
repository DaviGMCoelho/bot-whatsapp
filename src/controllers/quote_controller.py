from src.services.quote_service import QuoteService
from src.domains.models.DTOs.quotes.create_quote_dto import CreateQuoteRequestDTO

class QuoteController:
    def __init__(self, service: QuoteService):
        self.service = service

    def add(self, request: dict):
        company_id = int(request.get('company_id'))
        quote = CreateQuoteRequestDTO(
            quote = request.get('quote_text'),
            company_id = company_id,
            quote_type = request.get('quote_type'),
            active = request.get('active')
        )
        return self.service.add_quote(quote)
