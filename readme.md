# FAQs Chatbot

A simple semantic search system for finding answers in FAQ documents. Uses embeddings and vector similarity to retrieve relevant answers from documents.

## What does it do?

Loads FAQ documents, breaks them into chunks, generates embeddings, and allows you to search for relevant answers based on queries. Currently supports `.txt` and `.pdf` files.

## Setup

### Prerequisites
- Python 3.9+
- pip

### Installation

1. **Create virtual environment:**
   ```
   python -m venv venv
   ```

2. **Activate virtual environment:**
   
   On Windows:
   ```
   venv\Scripts\activate
   ```
   
   On Mac/Linux:
   ```
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Running the API Server

Start the FastAPI server with auto-reload:

```
uvicorn app.main:app --reload
```

Server runs on `http://localhost:8000`

API docs available at `http://localhost:8000/docs`

## API Endpoints

### 1. Home
```
GET /
```
Health check endpoint.

### 2. Upload Document
```
POST /upload
```
Upload a `.pdf` or `.txt` file to process and store in the vector database.

**Example:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@your_document.txt"
```

### 3. Query
```
POST /query
```
Ask a question and get relevant answers from stored documents.

**Body:**
```json
{
  "question": "How many vacation days do employees get?",
  "top_k": 3
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "How many vacation days?", "top_k": 3}'
```

## Testing

To test the whole pipeline manually (load document → chunk → embed → search):

```
python test_pipeline.py
```

This will:
- Load the sample FAQ document
- Split it into chunks
- Generate embeddings
- Store them in the vector database
- Run a sample query and show search results

## Project Structure

```
FAQs-Chatbot/
├── app/
│   ├── main.py               # FastAPI application & endpoints
│   ├── qa_service.py         # Document ingestion & querying logic
│   ├── document_loader.py    # Load PDF/TXT files
│   ├── chunker.py            # Split text into chunks
│   ├── embedder.py           # Generate embeddings
│   └── vector_store.py       # FAISS vector store
├── uploaded_docs/            # Storage for uploaded documents
├── test_pipeline.py          # Standalone pipeline test
├── requirements.txt          # Dependencies
└── readme.md                 # This file
```

