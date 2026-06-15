from typing import List

from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"


class EmbeddingClient:
    def __init__(self):
        self.client = OpenAI()

    def embed(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
        return [item.embedding for item in response.data]

    def embed_one(self, text: str) -> List[float]:
        return self.embed([text])[0]
