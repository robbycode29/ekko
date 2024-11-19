from pinecone import Pinecone
from bot.settings import PINECONE_TOKEN, PINECONE_INDEX

from typing import List

import uuid


class PineconeInterface:
    def __init__(self):
        self.pinecone = Pinecone(api_key=PINECONE_TOKEN)
        self.index_name = PINECONE_INDEX

    def _connect_to_index(self):
        return self.pinecone.Index(self.index_name)

    def upsert(self, vectors: List[List[float]]):
        index = self._connect_to_index()
        data = [{"id": str(uuid.uuid4()), "values": vector} for vector in vectors]
        index.upsert(data)

    def query(self, vector: List[float], top_k: int = 5):
        index = self._connect_to_index()
        results = index.query(queries=[vector], top_k=top_k)
        return results[0].matches
