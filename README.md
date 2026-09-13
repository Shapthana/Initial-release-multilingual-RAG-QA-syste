\# Multilingual RAG-Based Document Question Answering \& Evaluation System



A research-oriented Retrieval-Augmented Generation (RAG) system for multilingual document question answering across \*\*English, Sinhala, and Tamil\*\*.



The project focuses primarily on \*\*retrieval quality, multilingual robustness, and systematic evaluation\*\* rather than treating generation quality as the only measure of a RAG system.



\## Research Objective



The main objective is to investigate how different information-retrieval strategies perform for multilingual question answering, particularly when English, Sinhala, and Tamil queries are used.



The system compares:



\* BM25 lexical retrieval

\* Multilingual dense retrieval using E5 embeddings

\* Weighted hybrid retrieval

\* Reciprocal Rank Fusion (RRF)

\* Optional cross-encoder reranking



Retrieval performance is evaluated using:



\* Recall@5

\* Recall@10

\* Mean Reciprocal Rank (MRR)

\* nDCG@10



\## System Architecture



```text

&#x20;                   ┌─────────────────────┐

&#x20;                   │   User Question     │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │ Query Processing    │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                ┌─────────────┴─────────────┐

&#x20;                ▼                           ▼

&#x20;       ┌────────────────┐          ┌────────────────┐

&#x20;       │ BM25 Retrieval │          │ Dense Retrieval│

&#x20;       │   (Lexical)    │          │  (E5 + FAISS) │

&#x20;       └───────┬────────┘          └────────┬───────┘

&#x20;               │                            │

&#x20;               └────────────┬───────────────┘

&#x20;                            ▼

&#x20;                  ┌─────────────────────┐

&#x20;                  │ Hybrid / RRF Fusion │

&#x20;                  └──────────┬──────────┘

&#x20;                             │

&#x20;                             ▼

&#x20;                  ┌─────────────────────┐

&#x20;                  │ Optional Reranking  │

&#x20;                  └──────────┬──────────┘

&#x20;                             │

&#x20;                             ▼

&#x20;                  ┌─────────────────────┐

&#x20;                  │ Retrieved Context   │

&#x20;                  └──────────┬──────────┘

&#x20;                             │

&#x20;                             ▼

&#x20;                  ┌─────────────────────┐

&#x20;                  │ LLM Generation      │

&#x20;                  │     Qwen3-4B        │

&#x20;                  └─────────────────────┘

```



\## Languages



| Language  | Evaluation Questions |

| --------- | -------------------: |

| English   |                   20 |

| Sinhala   |                   20 |

| Tamil     |                   20 |

| \*\*Total\*\* |               \*\*60\*\* |



The evaluation benchmark contains 60 questions distributed equally across the three languages.



\## Retrieval Benchmark



The main benchmark compares BM25, multilingual dense retrieval using E5 embeddings, weighted hybrid retrieval, and Reciprocal Rank Fusion.



| Method           |   Recall@5 |  Recall@10 |        MRR |    nDCG@10 |

| ---------------- | ---------: | ---------: | ---------: | ---------: |

| BM25             |     0.9667 |     1.0000 |     0.8556 |     0.8920 |

| Dense E5         |     1.0000 |     1.0000 |     0.8117 |     0.8602 |

| E5 Hybrid α=0.75 |     1.0000 |     1.0000 |     0.9033 |     0.9283 |

| E5 + RRF         | \*\*0.9833\*\* | \*\*1.0000\*\* | \*\*0.9125\*\* | \*\*0.9345\*\* |



\### Main Finding



\*\*E5 + Reciprocal Rank Fusion produced the strongest overall ranking quality\*\*, achieving:



\* Recall@5: \*\*0.9833\*\*

\* Recall@10: \*\*1.0000\*\*

\* MRR: \*\*0.9125\*\*

\* nDCG@10: \*\*0.9345\*\*



Although dense E5 retrieval achieved perfect Recall@5 and Recall@10, RRF produced better ranking quality according to MRR and nDCG@10.



\## Language-Specific Analysis



The experiments also examined differences between languages.



\### English



Dense retrieval performed strongly for English queries, while hybrid retrieval achieved perfect ranking on the evaluated benchmark.



\### Sinhala



Sinhala was the most important retrieval challenge.



Dense E5 retrieval showed weaker ranking performance for Sinhala than BM25:



\* BM25 MRR: \*\*0.8167\*\*

\* Dense E5 MRR: \*\*0.6350\*\*

\* E5 + RRF MRR: \*\*0.8458\*\*



This suggests that lexical retrieval provided useful signals for Sinhala queries that were not consistently captured by dense retrieval.



\### Tamil



Tamil retrieval was strong overall, with BM25 performing particularly well and RRF maintaining strong ranking performance.



\## Hybrid Retrieval Experiment



A weighted hybrid approach was evaluated using different values of α to combine BM25 and dense retrieval.



The best tested configuration was:



\*\*α = 0.75\*\*



This configuration achieved:



\* Recall@5: \*\*1.0000\*\*

\* Recall@10: \*\*1.0000\*\*

\* MRR: \*\*0.9033\*\*

\* nDCG@10: \*\*0.9283\*\*



The experiment demonstrates that combining lexical and semantic retrieval can improve ranking quality compared with either retrieval method alone.



\## Reciprocal Rank Fusion



RRF was evaluated as an alternative to directly combining normalized retrieval scores.



The E5 + RRF configuration achieved the strongest overall MRR and nDCG@10 in the benchmark:



\* MRR: \*\*0.9125\*\*

\* nDCG@10: \*\*0.9345\*\*



This indicates that rank-based fusion was effective for combining complementary retrieval signals.



\## Reranking Experiment



A multilingual cross-encoder reranker was also investigated using:



`cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`



The experiment did not consistently improve retrieval performance.



This was treated as a useful negative/limited experiment rather than selecting a more complex model simply because it was expected to perform better.



\## Generation Experiment



The project also integrates \*\*Qwen3-4B through Ollama\*\* for local answer generation.



Generation evaluation was conducted as a preliminary experiment using:



\* Token F1

\* Context word support

\* Citation grounding

\* Retrieval latency

\* Generation latency



The generation results varied substantially between questions, including occasional incomplete responses and reasoning-text leakage.



Therefore, generation metrics are treated as \*\*preliminary evidence\*\*, while retrieval metrics form the primary evaluation of the research project.



\## Evaluation Data



The project contains:



```text

data/

├── documents/

│   ├── academic\_calendar.txt

│   ├── course\_module\_handbook.txt

│   ├── examination\_regulations.txt

│   ├── faculty\_handbook.txt

│   ├── institutional\_services\_guide.txt

│   ├── library\_regulations.txt

│   ├── research\_innovation\_policy.txt

│   ├── scholarship\_student\_support.txt

│   └── university\_student\_handbook.txt

│

├── evaluation/

│   ├── evaluation.baseline.jsonl

│   ├── evaluation.enriched.jsonl

│   └── evaluation.example.jsonl

│

└── results/

&#x20;   ├── failure\_analysis.json

&#x20;   ├── generation\_evaluation.json

&#x20;   └── retrieval\_benchmark.json

```



The document corpus is a \*\*synthetic research corpus\*\* created for controlled experimentation.



\## Project Structure



```text

backend/

├── app/

│   ├── api/

│   ├── services/

│   │   ├── chunker.py

│   │   ├── evaluator.py

│   │   ├── generator.py

│   │   ├── loader.py

│   │   ├── reranker.py

│   │   └── retrieval.py

│   ├── config.py

│   └── main.py

│

├── data/

│   ├── documents/

│   ├── evaluation/

│   └── results/

│

├── scripts/

│   ├── evaluate.py

│   ├── evaluate\_generation.py

│   ├── failure\_analysis.py

│   ├── ingest.py

│   ├── run\_experiments.py

│   ├── run\_full\_research.py

│   └── validate\_evaluation.py

│

├── tests/

│   ├── test\_metrics.py

│   └── test\_retrieval\_logic.py

│

├── requirements.txt

└── README.md

```



\## Installation



\### 1. Clone the repository



```bash

git clone https://github.com/Shapthana/Initial-release-multilingual-RAG-QA-syste.git

cd Initial-release-multilingual-RAG-QA-syste

```



\### 2. Create a virtual environment



Windows PowerShell:



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```powershell

pip install -r requirements.txt

```



\## Build the Retrieval Index



From the project directory:



```powershell

python scripts/ingest.py

```



This prepares the document chunks and retrieval index used by the evaluation pipeline.



\## Run Retrieval Evaluation



Validate the evaluation data:



```powershell

python scripts/validate\_evaluation.py

```



Run the benchmark:



```powershell

python scripts/evaluate.py

```



\## Run Research Experiments



The project also includes scripts for running the retrieval experiments:



```powershell

python scripts/run\_experiments.py

```



For the complete research workflow:



```powershell

python scripts/run\_full\_research.py

```



\## Run Tests



Install pytest if it is not already installed:



```powershell

pip install pytest

```



Then run:



```powershell

pytest -q

```



\## Generation



The project can use Ollama for local LLM generation.



The tested model was:



```text

Qwen3-4B

```



Generation experiments can be run using:



```powershell

python scripts/evaluate\_generation.py

```



\## Research Limitations



The current evaluation has several limitations:



1\. The benchmark contains 60 questions and is relatively small.

2\. The document corpus is synthetic and controlled rather than a large real-world collection.

3\. Sinhala and Tamil retrieval require further investigation on larger and more diverse datasets.

4\. Generation evaluation is preliminary.

5\. Cross-encoder reranking did not consistently improve the tested configuration.



\## Future Work



Future experiments could investigate:



\* Larger multilingual document collections

\* More Sinhala and Tamil evaluation questions

\* Human evaluation of answer faithfulness and correctness

\* Better multilingual embedding models

\* Alternative reranking models

\* Query expansion

\* Language-specific retrieval strategies

\* More robust citation evaluation

\* Larger-scale latency and memory benchmarking



\## Research Takeaway



The experiments show that multilingual RAG retrieval should not be evaluated using a single retrieval method or a single aggregate metric.



In this benchmark, lexical and semantic retrieval exhibited different strengths across languages. Rank-based fusion using RRF provided the strongest overall ranking quality, while Sinhala highlighted an important weakness of dense retrieval that was partially addressed through fusion with lexical retrieval.



\## Technologies



\* Python

\* FastAPI

\* BM25

\* FAISS

\* Sentence Transformers

\* Multilingual embeddings

\* Cross-encoder reranking

\* Ollama

\* Qwen3-4B

\* NumPy

\* scikit-learn

\* Pytest



\## Author



\*\*Shapthana Jeganathan\*\*



Computer Engineering Undergraduate

University of Jaffna



GitHub:

https://github.com/Shapthana/Initial-release-multilingual-RAG-QA-syste



