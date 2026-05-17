from app.document_loader import load_document
from app.chunker import chunk_text
from app.embedder import generate_embeddings, generate_query_embedding
from app.vector_store import VectorStore
import os

file_path = "uploaded_docs/sample.txt"

text = load_document(file_path)
chunks = chunk_text(text, chunk_size=10, overlap=3)

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

vector_store = VectorStore(dimension)

vector_store.add_embeddings(embeddings, metadata)

query = "How many vacation days do employees get?"

query_embedding = generate_query_embedding(query)

results = vector_store.search(query_embedding, top_k=3)

print("Total chunks:", len(chunks))
print("Question:", query)

print("\nSearch Results:")

for result in results:
    print("\n--- Result ---")
    print("File:", result["file_name"])
    print("Chunk ID:", result["chunk_id"])
    print("Distance:", result["distance"])
    print("Text:")
    print(result["text"])

