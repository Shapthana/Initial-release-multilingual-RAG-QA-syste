from pathlib import Path
import json,sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.services.retrieval import HybridRetriever
from app.services.evaluator import reciprocal_rank
ROOT=Path(__file__).resolve().parents[1]; INDEX=ROOT/"data"/"index"; EVAL=ROOT/"data"/"evaluation"/"evaluation.enriched.jsonl"

def rank(rs,rel):
    ids=[x["id"] for x in rs]; rr=reciprocal_rank(ids,rel); return int(round(1/rr)) if rr else None
def main():
    r=HybridRetriever(); r.load(INDEX/"faiss.index",INDEX/"metadata.json")
    rows=[json.loads(x) for x in EVAL.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
    cases=[]
    for row in rows:
        rel=set(row["relevant_chunk_ids"]); b=r.bm25_search(row["question"],10); d=r.dense_search(row["question"],10); h=r.hybrid_search(row["question"],10,0.5)
        br,dr,hr=rank(b,rel),rank(d,rel),rank(h,rel)
        if br is None and dr is not None: kind="dense_only"
        elif dr is None and br is not None: kind="bm25_only"
        elif br is not None and dr is not None and abs(br-dr)>=3: kind="ranking_gap"
        elif hr is None and (br is not None or dr is not None): kind="hybrid_regression"
        else: continue
        cases.append({"id":row["id"],"language":row.get("language"),"question_type":row.get("question_type","unknown"),"question":row["question"],"relevant_chunk_ids":list(rel),"bm25_rank":br,"dense_rank":dr,"hybrid_rank":hr,"case":kind,"bm25_top5":[x["id"] for x in b[:5]],"dense_top5":[x["id"] for x in d[:5]],"hybrid_top5":[x["id"] for x in h[:5]]})
    out=ROOT/"data"/"results"/"failure_analysis.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Interesting cases: {len(cases)}")
    for k in sorted({c["case"] for c in cases}): print(k,sum(c["case"]==k for c in cases))
if __name__=="__main__": main()
