import os

from app.document_loader import load_document
from app.chunker import chunk_text
from app.embedder import generate_embeddings, generate_query_embedding
from app.vector_store import VectorStore


vector_store = None


def ingest_document(file_path: str):

    global vector_store

    text = load_document(file_path)

    chunks = chunk_text(text, chunk_size=50, overlap=1)

    if not chunks:
        raise ValueError("No text chunks were created from this document.")

    metadata = []

    file_name = os.path.basename(file_path)

    for chunk_id, chunk in enumerate(chunks):
        metadata.append(
            {
                "text": chunk,
                "file_name": file_name,
                "chunk_id": chunk_id
            }
        )

    embeddings = generate_embeddings(chunks)

    dimension = embeddings.shape[1]

    if vector_store is None:
        vector_store = VectorStore(dimension)

    vector_store.add_embeddings(embeddings, metadata)

    return {
        "file_name": file_name,
        "chunks_created": len(chunks),
        "message": "Document ingested successfully"
    }


def answer_question(question: str, top_k: int = 3):

    if vector_store is None:
        raise ValueError("No documents have been uploaded yet.")

    query_embedding = generate_query_embedding(question)

    results = vector_store.search(query_embedding, top_k=top_k)

    return {
        "question": question,
        "results": results
    }

def reset_vector_store():

    global vector_store

    vector_store = None

    return {
        "message": "Vector store reset successfully"
    }