import os
import pdfplumber


def extract_text_from_pdf(file_path: str) -> str:
    full_text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                full_text += page_text + "\n"

    return full_text


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text


def load_document(file_path: str) -> str:
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif file_extension == ".txt":
        return extract_text_from_txt(file_path)

    else:
        raise ValueError(f"Unsupported file type: {file_extension}")