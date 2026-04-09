from src.database.chroma_db.connection import ChromaConn

class ChromaCollection:
    def __init__(self, client: ChromaConn):
        self.client = client.chroma
        self.products = None
        self.company = None
        self.user_memory = None
        self.conversation = None

    def init_collections(self):
        self.products = self.client.get_or_create_collection("products_embeddings")
        self.company = self.client.get_or_create_collection("company_knowledge")
        self.user_memory = self.client.get_or_create_collection("user_memory")
        self.conversation = self.client.get_or_create_collection("conversation_memory")
