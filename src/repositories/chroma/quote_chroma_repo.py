from src.database.chroma_db.collection import ChromaCollection
from src.domains.models.DTOs.quotes.create_quote_chroma_dto import CreateChromaQuoteDTO

class QuoteChromaRepository:
    def __init__(self, chroma_database: ChromaCollection):
        self.conn = chroma_database

    def _create_quote_description(self, quote_dict: dict):
        description = f'''
        Citação: {quote_dict['quote']}
        Categoria: {quote_dict['quote_type']}
        Citação para quem precisa de assuntos relacionados da categoria {quote_dict['quote_type']}.'''
        return description

    def upsert_quote(self, dto: CreateChromaQuoteDTO):
        description = self._create_quote_description(dto.to_dict())
        self.conn.company.upsert(
            ids = [dto.quote_id],
            documents = [description],
            metadatas = [{
                "quote_id": dto.quote_id,
                "company_id": dto.company_id,
                "quote_type": dto.quote_type,
                "code": dto.code
            }]
        )

    def delete_quote(self, quote_id: str):
        self.conn.company.delete(ids = [quote_id])

    def get_quote(self, quote_id: str, company_id: int):
        response = self.conn.company.get(
            ids = [quote_id]
        )
        return response
