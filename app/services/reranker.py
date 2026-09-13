from sentence_transformers import CrossEncoder

from app.config import RERANKER_MODEL


class Reranker:

    def __init__(self, model_name=RERANKER_MODEL):
        print(f"Loading reranker: {model_name}")

        self.model = CrossEncoder(model_name)

    def rerank(self, query, documents, top_k=5):
        if not documents:
            return []

        pairs = [
            [query, document["text"]]
            for document in documents
        ]

        scores = self.model.predict(pairs)

        results = []

        for document, score in zip(documents, scores):
            item = document.copy()
            item["reranker_score"] = float(score)
            results.append(item)

        results.sort(
            key=lambda x: x["reranker_score"],
            reverse=True
        )

        return results[:top_k]