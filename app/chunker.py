import re


def split_into_sentences(text: str) -> list[str]:

    text = text.replace("\n", " ")

    sentences = re.split(r"(?<=[.!?])\s+", text)

    clean_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if sentence:
            clean_sentences.append(sentence)

    return clean_sentences


def chunk_text(text: str, chunk_size: int = 80, overlap: int = 1) -> list[str]:

    sentences = split_into_sentences(text)

    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        sentence_word_count = len(sentence.split())

        if current_word_count + sentence_word_count <= chunk_size:
            current_chunk.append(sentence)
            current_word_count += sentence_word_count

        else:
            chunk = " ".join(current_chunk)

            if chunk:
                chunks.append(chunk)

            if overlap > 0:
                current_chunk = current_chunk[-overlap:]
                current_word_count = sum(len(s.split()) for s in current_chunk)
            else:
                current_chunk = []
                current_word_count = 0

            current_chunk.append(sentence)
            current_word_count += sentence_word_count

    if current_chunk:
        chunk = " ".join(current_chunk)
        chunks.append(chunk)

    return chunks