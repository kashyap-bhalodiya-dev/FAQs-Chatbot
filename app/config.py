import os
from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 50))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 1))
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", 3))

LLM_MAX_CONTEXTS = int(os.getenv("LLM_MAX_CONTEXTS", 3))
MIN_RELEVANCE_SCORE = float(os.getenv("MIN_RELEVANCE_SCORE", 0.35))

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_docs")