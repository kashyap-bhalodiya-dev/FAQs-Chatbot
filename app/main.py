import os
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.qa_service import ingest_document, answer_question


app = FastAPI(
    title="FAQs - Chatbot",
    description="Upload documents and ask questions using FAISS-based semantic search.",
    version="1.0.0"
)


UPLOAD_DIR = "uploaded_docs"


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3


@app.get("/")
def home():
    return {
        "message": "Multi-Document Semantic Search API is running"
    }


@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = ingest_document(file_path)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
def query_document(request: QueryRequest):
    try:
        result = answer_question(
            question=request.question,
            top_k=request.top_k
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))