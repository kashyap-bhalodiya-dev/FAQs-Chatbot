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

## Running the Test Pipeline

To test the whole pipeline (load document → chunk → embed → search):

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
│   ├── document_loader.py    # Load PDF/TXT files
│   ├── chunker.py            # Split text into chunks
│   ├── embedder.py           # Generate embeddings
│   ├── vector_store.py       # FAISS vector store
├── uploaded_docs/            # Sample documents
├── test_pipeline.py          # Test the full pipeline
├── requirements.txt          # Dependencies
└── readme.md                 # This file
```

