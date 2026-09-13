from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]
INPUT_FILE=ROOT/"data"/"evaluation"/"evaluation.example.jsonl"
OUTPUT_FILE=ROOT/"data"/"evaluation"/"evaluation.enriched.jsonl"

def classify_question(question):
    q=question.lower()
    if re.search(r"\b(what are|which|list|sections)\b",q): return "list"
    if re.search(r"\b(when|what time|how long|date|deadline|hours)\b",q): return "temporal"
    if re.search(r"\b(allowed|permitted|can i|may i|prohibited|not allowed)\b",q): return "permission"
    if re.search(r"\b(how|what should|what must|steps|process)\b",q): return "procedural"
    # Script-aware fallback for Sinhala/Tamil; labels are coarse and reproducible.
    if any(0x0D80 <= ord(c) <= 0x0DFF for c in question):
        if any(x in question for x in ["කවදා","වේලාව","පැය"]): return "temporal"
        if any(x in question for x in ["කෙසේ","කළ යුතු","කරන්නේ"]): return "procedural"
        if any(x in question for x in ["කුමන","මොනවාද","කොටස්"]): return "list"
    if any(0x0B80 <= ord(c) <= 0x0BFF for c in question):
        if any(x in question for x in ["எப்போது","நேரம்","மணி"]): return "temporal"
        if any(x in question for x in ["எப்படி","செய்ய வேண்டும்","செய்வது"]): return "procedural"
        if any(x in question for x in ["எவை","என்னென்ன","பகுதிகள்"]): return "list"
    return "factual"

def load_metadata():
    candidates=[ROOT/"data"/"index"/"metadata.json"]
    for p in candidates:
        if p.exists(): return {x["id"]:x for x in json.loads(p.read_text(encoding="utf-8-sig"))}
    return {}

def main():
    rows=[json.loads(x) for x in INPUT_FILE.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
    meta=load_metadata(); enriched=[]
    for row in rows:
        source_langs={meta[c]["language"] for c in row.get("relevant_chunk_ids",[]) if c in meta}
        source_lang=next(iter(source_langs)) if len(source_langs)==1 else ("mixed" if source_langs else "unknown")
        item=dict(row); item["question_type"]=classify_question(row["question"]); item["document_language"]=source_lang
        item["retrieval_type"]="monolingual" if source_lang==row.get("language") else "cross_lingual"
        enriched.append(item)
    OUTPUT_FILE.write_text("".join(json.dumps(x,ensure_ascii=False)+"\n" for x in enriched),encoding="utf-8-sig")
    print(f"Created {OUTPUT_FILE} with {len(enriched)} questions.")

if __name__=="__main__": main()
