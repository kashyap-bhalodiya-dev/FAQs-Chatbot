import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension: int):

        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.metadata = []

    def add_embeddings(self, embeddings: np.ndarray, metadata: list[dict]):

        self.index.add(embeddings)
        self.metadata.extend(metadata)

    def search(self, query_embedding: np.ndarray, top_k: int = 1):
    
        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, index in zip(distances[0], indices[0]):
            item = self.metadata[index]
            result = {
                "text": item["text"],
                "file_name": item["file_name"],
                "chunk_id": item["chunk_id"],
                "score": float(score),
                "index": int(index)
            }

            results.append(result)

        return results