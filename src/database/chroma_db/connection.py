import chromadb

class ChromaConn:
    def __init__(self, host: str, port: int):
        self.chroma = chromadb.HttpClient(host=host, port=port)
