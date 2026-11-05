from typing import List

from openai import OpenAI

from observability.tracing import trace_llm_call

EMBEDDING_MODEL = "text-embedding-3-small"


class EmbeddingClient:
    def __init__(self):
        self.client = OpenAI()

    def embed(self, texts: List[str]) -> List[List[float]]:
        with trace_llm_call("embed", "embedding", EMBEDDING_MODEL, texts) as span:
            response = self.client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
            span.update(usage_details={"input": response.usage.prompt_tokens})
        return [item.embedding for item in response.data]

    def embed_one(self, text: str) -> List[float]:
        return self.embed([text])[0]
