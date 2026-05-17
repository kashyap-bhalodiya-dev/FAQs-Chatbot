from sentence_transformers import SentenceTransformer
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(texts: list[str]) -> np.ndarray:

    embeddings = model.encode(texts)

    embeddings = np.array(embeddings).astype("float32")

    return embeddings


def generate_query_embedding(question: str) -> np.ndarray:

    embedding = model.encode([question])

    embedding = np.array(embedding).astype("float32")

    return embedding