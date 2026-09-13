from pathlib import Path

from pypdf import PdfReader

SUPPORTED = {".pdf", ".txt"}

def read_document(path: Path) -> str:

    if path.suffix.lower() == ".txt":

        return path.read_text(encoding="utf-8-sig", errors="strict")

    if path.suffix.lower() == ".pdf":

        reader = PdfReader(str(path))

        return "\n".join(page.extract_text() or "" for page in reader.pages)

    return ""