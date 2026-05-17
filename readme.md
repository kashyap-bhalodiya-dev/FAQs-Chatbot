# FAQs Chatbot

A simple semantic search system for finding answers in FAQ documents. Uses embeddings and FAISS for retrieval, and optionally feeds retrieved context into an LLM to generate cleaner answers.

## What does it do?

Loads FAQ documents, breaks them into sentence-based chunks, generates embeddings, and allows you to search for relevant answers based on queries. Sentence boundaries are detected using `.`, `!`, and `?`, so chunking respects natural sentence breaks.

There are two query modes:
- `/query`: returns similarity search results directly
- `/ask`: uses an LLM to generate a cleaner answer from the retrieved context

Currently supports `.txt` and `.pdf` files.

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

4. **Add LLM credentials (optional):**
   - Create a `.env` file in the project root
   - Add `GEMINI_API_KEY` and optionally `GEMINI_MODEL`
   
   Example:
   ```text
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
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

### 2. Reset Index
```
POST /reset
```
Reset the current in-memory FAISS index and clear all ingested documents from the current session.

**Example:**
```bash
curl -X POST "http://localhost:8000/reset"
```

### 3. Upload Document
```
POST /upload
```
Upload a `.pdf` or `.txt` file to process and store in the vector database.

**Example:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@your_document.txt"
```

### 4. Query
```
POST /query
```
Ask a question and get raw similarity search results from stored documents. This returns matching chunks and relevance scores.

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

### 5. Ask (LLM-enhanced)
```
POST /ask
```
Ask a question and get a generated answer from the LLM using retrieved document context. This is the preferred route for natural responses.

**Body:**
```json
{
  "question": "How many vacation days do employees get?",
  "top_k": 3
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/ask" \
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
- Split it into sentence-based chunks
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
│   ├── llm_service.py        # LLM prompt and answer generation
│   ├── config.py            # App configuration and environment settings
│   └── vector_store.py       # FAISS vector store
├── uploaded_docs/            # Storage for uploaded documents
├── test_pipeline.py          # Standalone pipeline test
├── requirements.txt          # Dependencies
```

