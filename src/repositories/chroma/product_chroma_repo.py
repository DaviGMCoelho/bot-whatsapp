from src.database.chroma_db.collection import ChromaCollection
from src.domains.models.DTOs.item.create_chroma_item_dto import CreateChromaItemDTO
from src.domains.models.DTOs.item.update_chroma_item_dto import UpdateChromaItemDTO

class ProductChromaRepository:
    def __init__ (self, chroma_database: ChromaCollection):
        self.conn = chroma_database

    def _create_product_description(self, product_dict: dict):
        description = f'''
        Produto: {product_dict['name']}
        Descrição: {product_dict['description']}
        Categoria: {product_dict['catalog_name']}
        Produto ideal para quem procura itens da categoria {product_dict['catalog_name']}.'''
        return description

    def upsert_product(self, create_chroma_item: CreateChromaItemDTO):
        description = self._create_product_description(create_chroma_item.to_dict())
        self.conn.products.upsert(
            ids = [create_chroma_item.item_id],
            documents = [description],
            metadatas = [{
                "product_id": create_chroma_item.item_id,
                "code": create_chroma_item.code,
                "company_id": create_chroma_item.company_id
            }]
        )

    def get_product(self, product_id: str, company_id: int):
        response = self.conn.products.query(
            where = {'product_id': product_id, 'company_id': company_id}
            )
        return response

    def update_product(self, update_chroma_item: UpdateChromaItemDTO):
        description = self._create_product_description(update_chroma_item.to_dict())
        self.conn.products.upsert(
            ids = [f'product_{update_chroma_item.product_id}'],
            documents = [description],
            metadatas = [{
                "product_id": update_chroma_item.product_id,
                "code": update_chroma_item.code,
                "company_id": update_chroma_item.company_id
            }]
        )

    def delete_product(self, product_id: str):
        print(f'ariuepa - {product_id}')
        self.conn.products.delete(ids = [product_id])
