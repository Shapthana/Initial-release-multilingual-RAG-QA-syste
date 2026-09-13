# Multilingual Retrieval for RAG-Based Document Question Answering

## Problem
Multilingual document QA depends heavily on retrieval quality. A system can generate fluent answers while still failing if the relevant chunk is ranked poorly. This study treats retrieval as the main experimental problem and compares sparse, dense, and hybrid retrieval for English, Sinhala, and Tamil.

## Research gap and question
The study focuses on language-specific retrieval robustness: how retrieval signals behave differently across languages and what failures explain those differences.

**Research question:** How do sparse, dense, and hybrid retrieval methods differ in retrieval effectiveness across English, Sinhala, and Tamil, and what language-specific retrieval failures explain the differences?

## Method
A fixed multilingual evaluation set is paired with a controlled synthetic document corpus. BM25 provides the lexical baseline. A multilingual sentence-transformer provides dense embeddings indexed with FAISS. Hybrid retrieval combines normalized BM25 and dense scores using a controlled alpha sweep. RRF and optional CrossEncoder reranking provide additional comparisons.

## Results
Populate this table only from `data/results/retrieval_benchmark.json`.

| Method | Recall@5 | Recall@10 | MRR | nDCG@10 |
|---|---:|---:|---:|---:|
| BM25 | | | | |
| Dense | | | | |
| Hybrid α=0.25 | | | | |
| Hybrid α=0.50 | | | | |
| Hybrid α=0.75 | | | | |
| RRF | | | | |
| RRF + reranker | | | | |

## Multilingual findings
Use the language-wise section of the generated benchmark JSON. Report differences between English, Sinhala, and Tamil without claiming statistical generalization beyond the controlled dataset.

## Failure analysis
Use `data/results/failure_analysis.json` to select 2–3 representative cases. Explain whether the failure is lexical mismatch, semantic mismatch, ranking instability, language-related behavior, or insufficient evidence.

## Answer evaluation
If `evaluate_generation.py` is run, report answer token-F1 only as a lexical proxy. Do not label the deterministic context-word-support score as human-validated faithfulness. Human or LLM-judge evaluation is required for a stronger faithfulness claim.

## Limitations and next work
The current corpus and evaluation set are controlled and relatively small. Future work should use a larger human-validated multilingual corpus, stronger language-specific relevance judgments, multiple embedding models, statistical significance testing, and human evaluation of answer faithfulness and citation correctness.
