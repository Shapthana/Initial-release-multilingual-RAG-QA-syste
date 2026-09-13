from pathlib import Path
import argparse, json, csv, time
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.services.retrieval import HybridRetriever
from app.services.reranker import Reranker
from app.services.evaluator import recall_at_k, reciprocal_rank, ndcg_at_k

ROOT=Path(__file__).resolve().parents[1]
EVAL=ROOT/"data"/"evaluation"/"evaluation.enriched.jsonl"
if not EVAL.exists(): EVAL=ROOT/"data"/"evaluation"/"evaluation.example.jsonl"

def load_rows(): return [json.loads(x) for x in EVAL.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
def metrics(ids, rel): return {"recall@5":recall_at_k(ids,rel,5),"recall@10":recall_at_k(ids,rel,10),"mrr":reciprocal_rank(ids,rel),"ndcg@10":ndcg_at_k(ids,rel,10)}
def avg(rows):
    if not rows:return {k:0.0 for k in ["recall@5","recall@10","mrr","ndcg@10","mean_latency_ms"]}
    return {**{k:round(sum(x[k] for x in rows)/len(rows),4) for k in ["recall@5","recall@10","mrr","ndcg@10"]},"mean_latency_ms":round(sum(x.get("latency_ms",0) for x in rows)/len(rows),2)}
def retrieve(r,q,method,alpha=0.5,rrf_k=60,k=10):
    if method=="bm25": return r.bm25_search(q,k)
    if method=="dense": return r.dense_search(q,k)
    if method=="hybrid": return r.hybrid_search(q,k,alpha)
    if method=="rrf": return r.rrf_search(q,k,rrf_k)
    raise ValueError(method)
def evaluate(r,rows,method,alpha=0.5):
    out=[]
    for row in rows:
        started=time.perf_counter(); rs=retrieve(r,row["question"],method,alpha,k=10); elapsed=(time.perf_counter()-started)*1000; m=metrics([x["id"] for x in rs],row["relevant_chunk_ids"]); out.append({**m,"id":row["id"],"language":row.get("language","unknown"),"question_type":row.get("question_type","unknown"),"latency_ms":elapsed})
    return out
def grouped(rows,key):
    vals=sorted(set(x.get(key,"unknown") for x in rows)); return {v:avg([x for x in rows if x.get(key,"unknown")==v]) for v in vals}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--index",default=""); ap.add_argument("--output",default="data/results/retrieval_benchmark.json"); ap.add_argument("--reranker",action="store_true"); args=ap.parse_args()
    index=ROOT/"data"/"index"/(args.index if args.index else "")
    r=HybridRetriever(); r.load(index/"faiss.index",index/"metadata.json"); rows=load_rows()
    results={}; per_query={}
    for method in ["bm25","dense","rrf"]:
        ms=evaluate(r,rows,method); results[method]=avg(ms); per_query[method]=ms
    for alpha in [0.0,0.25,0.5,0.75,1.0]:
        name=f"hybrid_{alpha:.2f}"; ms=evaluate(r,rows,"hybrid",alpha); results[name]=avg(ms); per_query[name]=ms
    best=max((x for x in results if x.startswith("hybrid_")),key=lambda x:(results[x]["mrr"],results[x]["ndcg@10"],results[x]["recall@5"]))
    if args.reranker:
        rr=Reranker(); ms=[]
        for row in rows:
            cand=r.rrf_search(row["question"],k=min(10,len(r.documents))); rer=rr.rerank(row["question"],cand,top_k=min(10,len(cand))); ms.append({**metrics([x["id"] for x in rer],row["relevant_chunk_ids"]),"id":row["id"],"language":row.get("language"),"question_type":row.get("question_type","unknown")})
        results["rrf_reranker"] = avg(ms); per_query["rrf_reranker"]=ms
    report={"dataset":{"path":str(EVAL.relative_to(ROOT)),"questions":len(rows),"languages":{l:sum(x.get("language")==l for x in rows) for l in ["en","si","ta"]},"note":"Controlled evaluation corpus; do not generalize beyond this dataset. Latency is measured locally and is hardware-dependent."},"overall":results,"best_hybrid":best,"language_wise":{m:grouped(ms,"language") for m,ms in per_query.items()},"query_type_wise":{m:grouped(ms,"question_type") for m,ms in per_query.items()},"per_query":per_query}
    out=ROOT/args.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"overall":results,"best_hybrid":best},indent=2))

if __name__=="__main__": main()
