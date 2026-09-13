# Research Plan

## Research gap
Multilingual RAG systems can exhibit language-dependent retrieval quality, especially when comparing high-resource English with lower-resource languages. A practical gap is understanding how sparse lexical retrieval, multilingual dense retrieval, and their combinations behave across English, Sinhala, and Tamil, and which ranking failures explain the differences.

## Research question
**How do sparse, dense, and hybrid retrieval methods differ in retrieval effectiveness across English, Sinhala, and Tamil, and what language-specific retrieval failures explain the differences?**

## Hypothesis
Hybrid retrieval may improve robustness by combining lexical matching with semantic similarity, but its benefit is expected to vary by language and query type.

## Experimental design
- Fixed evaluation set: English, Sinhala, Tamil questions with manually assigned relevant chunk IDs.
- Primary baselines: BM25 and multilingual dense retrieval using FAISS inner-product search over normalized embeddings.
- Hybrid: weighted min-max score fusion over the full indexed corpus; alpha ∈ {0, 0.25, 0.50, 0.75, 1.0}.
- Additional method: Reciprocal Rank Fusion (RRF, k=60).
- Optional reranking: CrossEncoder applied to the top-10 RRF candidate set.
- Controlled corpus: synthetic documents explicitly marked as synthetic; results are not presented as official university policy or production performance.

## Metrics
- Recall@5
- Recall@10
- MRR
- nDCG@10
- Language-wise metrics
- Query-type metrics
- Failure/disagreement cases
- Optional answer token-F1 proxy against reference answers
- Optional context-word support proxy and citation validation
- Latency can be added as a system measurement, but is not treated as a quality metric.

## Failure categories
- BM25-only success
- Dense-only success
- Ranking gap
- Hybrid regression
- Wrong document/chunk
- Language mismatch
- Insufficient context
- Generation/citation error

## Reproducibility rule
Record only results produced by the supplied scripts. Never invent benchmark numbers. Every reported result should identify the dataset, index/model, method, parameters, and date/run.
