from src.database.chroma_db.connection import ChromaConn

class ProductChromaRepository:
    def __init__ (self, chroma_connection: ChromaConn):
        self.conn = chroma_connection
