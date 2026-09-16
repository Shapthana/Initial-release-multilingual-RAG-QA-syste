from pathlib import Path
import json
import numpy as np

try:
    import faiss
except ImportError:
    faiss = None

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from app.config import EMBEDDING_MODEL


class HybridRetriever:
    """BM25 + multilingual dense retrieval with explicit score fusion and RRF."""

    def __init__(self, model_name=EMBEDDING_MODEL):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.is_e5 = "e5" in model_name.lower()
        self.documents = []
        self.bm25 = None
        self.index = None
        self.dimension = None

    def _embedding_text(self, text):
        return f"passage: {text}" if self.is_e5 else text

    def _embedding_query(self, query):
        return f"query: {query}" if self.is_e5 else query

    def fit(self, documents):
        if not documents:
            raise ValueError("No documents provided")
        self.documents = documents
        texts = [d["text"] for d in documents]
        self.bm25 = BM25Okapi([t.lower().split() for t in texts])

        vectors = self.model.encode(
            [self._embedding_text(t) for t in texts],
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=True,
        ).astype("float32")
        if faiss is None:
            raise RuntimeError("FAISS is not installed. Install faiss-cpu.")
        self.dimension = vectors.shape[1]
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(vectors)

    def bm25_search(self, query, k=10):
        if self.bm25 is None:
            return []
        k = min(max(1, k), len(self.documents))
        scores = self.bm25.get_scores(query.lower().split())
        # Stable tie handling: score desc, original document order asc.
        ids = sorted(range(len(scores)), key=lambda i: (-float(scores[i]), i))[:k]
        return [{**self.documents[i], "bm25_score": float(scores[i])} for i in ids]

    def dense_search(self, query, k=10):
        if self.index is None:
            return []
        k = min(max(1, k), len(self.documents))
        q = self.model.encode(
            [self._embedding_query(query)],
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).astype("float32")
        scores, ids = self.index.search(q, k)
        return [
            {**self.documents[i], "dense_score": float(score)}
            for score, i in zip(scores[0], ids[0]) if i >= 0
        ]

    @staticmethod
    def _minmax(values):
        if not values:
            return []
        lo, hi = min(values), max(values)
        if hi == lo:
            return [1.0] * len(values)
        return [(v - lo) / (hi - lo) for v in values]

    def hybrid_search(self, query, k=5, alpha=0.5):
        """Weighted min-max fusion over the full indexed corpus.

        alpha=0 is exactly BM25 and alpha=1 is exactly dense retrieval.
        For intermediate alpha values both systems score every indexed chunk,
        avoiding a changing candidate pool during the sweep.
        """
        if not 0.0 <= alpha <= 1.0:
            raise ValueError("alpha must be between 0.0 and 1.0")
        if alpha == 0.0:
            return self.bm25_search(query, k)
        if alpha == 1.0:
            return self.dense_search(query, k)
        if not self.documents:
            return []

        bm25 = self.bm25_search(query, len(self.documents))
        dense = self.dense_search(query, len(self.documents))
        bm25_norm = self._minmax([x["bm25_score"] for x in bm25])
        dense_norm = self._minmax([x["dense_score"] for x in dense])
        bm25_map = {x["id"]: (x, s) for x, s in zip(bm25, bm25_norm)}
        dense_map = {x["id"]: (x, s) for x, s in zip(dense, dense_norm)}

        merged=[]
        for doc in self.documents:
            did=doc["id"]
            b_item,b = bm25_map[did]
            d_item,d = dense_map[did]
            merged.append({
                **doc,
                "bm25_score": b_item["bm25_score"],
                "dense_score": d_item["dense_score"],
                "bm25_normalized": b,
                "dense_normalized": d,
                "hybrid_score": alpha*d + (1-alpha)*b,
            })
        merged.sort(key=lambda x: (-x["hybrid_score"], x["id"]))
        return merged[:max(1,k)]

    def rrf_search(self, query, k=5, rrf_k=60):
        if rrf_k <= 0:
            raise ValueError("rrf_k must be greater than 0")
        bm25 = self.bm25_search(query, len(self.documents))
        dense = self.dense_search(query, len(self.documents))
        scores = {d["id"]: 0.0 for d in self.documents}
        data = {d["id"]: d.copy() for d in self.documents}
        for rank,item in enumerate(bm25,1):
            scores[item["id"]] += 1.0/(rrf_k+rank)
            data[item["id"]].update(item)
        for rank,item in enumerate(dense,1):
            scores[item["id"]] += 1.0/(rrf_k+rank)
            data[item["id"]].update(item)
        ranked=sorted(scores, key=lambda did:(-scores[did],did))[:max(1,k)]
        out=[]
        for did in ranked:
            item=data[did]
            item["rrf_score"]=float(scores[did])
            out.append(item)
        return out

    def save(self,index_path:Path,metadata_path:Path):
        if self.index is None or faiss is None:
            raise RuntimeError("Retriever is not fitted or FAISS is unavailable")
        index_path.parent.mkdir(parents=True,exist_ok=True)
        faiss.write_index(self.index,str(index_path))
        metadata_path.write_text(json.dumps(self.documents,ensure_ascii=False,indent=2),encoding="utf-8")

    def load(self,index_path:Path,metadata_path:Path):
        if faiss is None:
            raise RuntimeError("FAISS is not installed")
        self.index=faiss.read_index(str(index_path))
        self.documents=json.loads(metadata_path.read_text(encoding="utf-8-sig"))
        self.bm25=BM25Okapi([d["text"].lower().split() for d in self.documents])
        self.dimension=self.index.d
