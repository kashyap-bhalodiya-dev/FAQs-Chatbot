import os

from app.document_loader import load_document
from app.chunker import chunk_text
from app.embedder import generate_embeddings, generate_query_embedding
from app.vector_store import VectorStore
from app.llm_service import generate_answer
from app.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    DEFAULT_TOP_K,
    LLM_MAX_CONTEXTS,
    MIN_RELEVANCE_SCORE
)


vector_store = None


def ingest_document(file_path: str):
    global vector_store

    text = load_document(file_path)

    chunks = chunk_text(
        text,
        chunk_size=CHUNK_SIZE,
        overlap=CHUNK_OVERLAP
    )

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


def answer_question(question: str, top_k: int = DEFAULT_TOP_K):

    if vector_store is None:
        raise ValueError("No documents have been uploaded yet.")

    query_embedding = generate_query_embedding(question)

    results = vector_store.search(query_embedding, top_k=top_k)

    return {
        "question": question,
        "results": results
    }


def filter_contexts_for_llm(results: list[dict]) -> list[dict]:

    filtered_results = []

    for result in results:
        if result["score"] >= MIN_RELEVANCE_SCORE:
            filtered_results.append(result)

    filtered_results = filtered_results[:LLM_MAX_CONTEXTS]

    return filtered_results


def answer_question_with_llm(question: str, top_k: int = DEFAULT_TOP_K):

    retrieval_result = answer_question(
        question=question,
        top_k=top_k
    )

    all_results = retrieval_result["results"]

    selected_contexts = filter_contexts_for_llm(all_results)

    if not selected_contexts:
        return {
            "question": question,
            "answer": "I could not find the answer in the uploaded documents.",
            "sources": [],
            "raw_results": all_results,
            "selected_contexts": []
        }

    llm_answer = generate_answer(
        question=question,
        contexts=selected_contexts
    )

    sources = []

    for item in selected_contexts:
        sources.append(
            {
                "file_name": item["file_name"],
                "chunk_id": item["chunk_id"],
                "score": item["score"],
                "index": item["index"]
            }
        )

    return {
        "question": question,
        "answer": llm_answer,
        "sources": sources,
        "raw_results": all_results,
        "selected_contexts": selected_contexts
    }

def reset_vector_store():

    global vector_store

    vector_store = None

    return {
        "message": "Vector store reset successfully"
    }