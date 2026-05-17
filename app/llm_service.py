from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL


def get_gemini_client():
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is missing. Please add it to your .env file."
        )

    return genai.Client(api_key=GEMINI_API_KEY)


def build_context_text(contexts: list[dict]) -> str:
    context_text = ""

    for context_number, item in enumerate(contexts, start=1):
        context_text += f"\nContext {context_number}:\n"
        context_text += f"Source File: {item['file_name']}\n"
        context_text += f"Chunk ID: {item['chunk_id']}\n"
        context_text += f"Relevance Score: {item['score']}\n"
        context_text += "Text:\n"
        context_text += item["text"]
        context_text += "\n"

    return context_text


def generate_answer(question: str, contexts: list[dict]) -> str:
    if not contexts:
        return "I could not find the answer in the uploaded documents."

    context_text = build_context_text(contexts)

    prompt = f"""
    You are a document question-answering assistant.

    Rules:
    1. Answer the user's question using ONLY the retrieved context.
    2. Do not use outside knowledge.
    3. Do not make assumptions.
    4. If the answer is not clearly present in the context, say:"I could not find the answer in the uploaded documents."
    5. Keep the answer concise and easy to understand.
    6. Mention the source file name at the end.

    User Question:
    {question}

    Retrieved Context:
    {context_text}

    Final Answer:
    """

    client = get_gemini_client()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text