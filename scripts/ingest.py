from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.services.loader import read_document, SUPPORTED
from app.services.chunker import chunk_text
from app.services.retrieval import HybridRetriever
from app.config import CHUNK_SIZE, CHUNK_OVERLAP

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/"data"/"documents"
DEFAULT_INDEX=ROOT/"data"/"index"


def detect_language(text):
    counts={"si":0,"ta":0,"en":0}
    for ch in text:
        cp=ord(ch)
        if 0x0D80 <= cp <= 0x0DFF: counts["si"] += 1
        elif 0x0B80 <= cp <= 0x0BFF: counts["ta"] += 1
        elif ch.isalpha() and ch.isascii(): counts["en"] += 1
    nonzero={k:v for k,v in counts.items() if v}
    if not nonzero: return "unknown"
    if len(nonzero)==1: return next(iter(nonzero))
    return max(nonzero,key=nonzero.get)


def build_index(index_dir):
    index_dir.mkdir(parents=True,exist_ok=True)
    records=[]
    for path in sorted(DOCS.iterdir()):
        if path.suffix.lower() not in SUPPORTED: continue
        text=read_document(path).strip()
        if not text: continue
        chunks=chunk_text(text,CHUNK_SIZE,CHUNK_OVERLAP)
        for i,chunk in enumerate(chunks):
            records.append({"id":f"{path.stem}-{i}","source":path.name,"text":chunk,"language":detect_language(chunk)})
    print(f"Loaded {len(records)} chunks.")
    if not records: raise SystemExit(f"Put PDF/TXT documents into {DOCS}")
    r=HybridRetriever(); r.fit(records); r.save(index_dir/"faiss.index",index_dir/"metadata.json")
    print(f"Saved index to {index_dir}")

if __name__=="__main__":
    name=sys.argv[1] if len(sys.argv)>1 else None
    build_index(DEFAULT_INDEX/name if name else DEFAULT_INDEX)
