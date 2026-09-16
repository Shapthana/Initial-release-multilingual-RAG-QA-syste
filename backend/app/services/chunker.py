def chunk_text(text: str, chunk_size: int = 50, overlap: int = 10):
    words = text.split()

    if not words:
        return []

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    step = chunk_size - overlap
    chunks = []

    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + chunk_size]).strip()

        if chunk:
            chunks.append(chunk)

    return chunks