import json
import os
from typing import Dict, List

import numpy as np

INDEX_PATH = os.path.join("rag", "index", "index.json")


class VectorStore:
    def __init__(self, path: str = INDEX_PATH):
        self.path = path
        self.chunks: List[Dict] = []

    def build(self, chunks: List[Dict]) -> None:
        self.chunks = chunks
        self.save()

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.chunks, f)

    def load(self) -> bool:
        if not os.path.exists(self.path):
            return False
        with open(self.path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)
        return True

    def search(self, query_embedding: List[float], top_k: int = 4) -> List[Dict]:
        if not self.chunks:
            return []

        matrix = np.array([c["embedding"] for c in self.chunks])
        query = np.array(query_embedding)

        norms = np.linalg.norm(matrix, axis=1) * np.linalg.norm(query)
        scores = (matrix @ query) / np.where(norms == 0, 1e-10, norms)

        top_indices = np.argsort(scores)[::-1][:top_k]
        return [
            {
                "source": self.chunks[i]["source"],
                "chunk_index": self.chunks[i]["chunk_index"],
                "text": self.chunks[i]["text"],
                "score": float(scores[i]),
            }
            for i in top_indices
        ]
