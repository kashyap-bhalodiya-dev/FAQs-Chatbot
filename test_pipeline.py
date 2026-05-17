from app.qa_service import ingest_document, answer_question


file_path = "uploaded_docs/sample.txt"

ingest_result = ingest_document(file_path)

print("Ingest Result:")
print(ingest_result)


question = "How many vacation days do employees get?"

answer = answer_question(question, top_k=3)

print("\nAnswer Result:")
print(answer)