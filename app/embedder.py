from sentence_transformers import SentenceTransformer
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(texts: list[str]) -> np.ndarray:

    embeddings = model.encode(texts, normalize_embeddings=True)

    embeddings = np.array(embeddings).astype("float32")

    return embeddings


def generate_query_embedding(question: str) -> np.ndarray:

    embedding = model.encode([question], normalize_embeddings=True)

    embedding = np.array(embedding).astype("float32")

    return embedding