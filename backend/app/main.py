from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.config import TOP_K, RERANKER_MODEL
from app.services.retrieval import HybridRetriever
from app.services.generator import generate_answer

ROOT=Path(__file__).resolve().parents[1]; INDEX_DIR=ROOT/"data/index"
app=FastAPI(title="Multilingual RAG Document QA",version="2.0.0")
retriever=HybridRetriever(); reranker=None

class QueryRequest(BaseModel):
    query:str=Field(min_length=1)
    k:int=Field(default=TOP_K,ge=1,le=20)
    method:str=Field(default="hybrid",pattern="^(bm25|dense|hybrid|rrf)$")
    alpha:float=Field(default=0.5,ge=0.0,le=1.0)
    use_reranker:bool=False

def retrieve(req):
    if not retriever.documents: raise HTTPException(503,"Index is not loaded. Run /reload after ingesting documents.")
    if req.method=="bm25": results=retriever.bm25_search(req.query,req.k*2)
    elif req.method=="dense": results=retriever.dense_search(req.query,req.k*2)
    elif req.method=="rrf": results=retriever.rrf_search(req.query,req.k*2)
    else: results=retriever.hybrid_search(req.query,req.k*2,req.alpha)
    if req.use_reranker:
        global reranker
        if reranker is None:
            from app.services.reranker import Reranker; reranker=Reranker(RERANKER_MODEL)
        results=reranker.rerank(req.query,results,req.k)
    else: results=results[:req.k]
    return results

@app.get("/health")
def health(): return {"status":"ok","documents":len(retriever.documents)}
@app.post("/reload")
def reload_index():
    index=INDEX_DIR/"faiss.index"; meta=INDEX_DIR/"metadata.json"
    if not index.exists() or not meta.exists(): return {"status":"missing","message":"Run scripts/ingest.py first."}
    retriever.load(index,meta); return {"status":"ok","documents":len(retriever.documents)}
@app.post("/retrieve")
def retrieve_endpoint(req:QueryRequest): return {"query":req.query,"method":req.method,"results":retrieve(req)}
@app.post("/ask")
def ask(req:QueryRequest):
    results=retrieve(req); return {"query":req.query,"method":req.method,"alpha":req.alpha,**generate_answer(req.query,results),"sources":results}
