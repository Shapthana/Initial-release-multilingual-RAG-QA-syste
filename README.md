# Multilingual RAG-Based Document Question Answering & Evaluation System

A research-oriented Retrieval-Augmented Generation (RAG) system for multilingual document question answering across **English, Sinhala, and Tamil**.

The project focuses primarily on **retrieval quality, multilingual robustness, controlled experimentation, and systematic evaluation**, rather than treating generation quality as the only measure of a RAG system.

## Research Objective

The main objective is to investigate how different information-retrieval strategies perform for multilingual question answering, particularly when English, Sinhala, and Tamil queries are used.

The system compares:

* BM25 lexical retrieval
* Multilingual dense retrieval using E5 embeddings
* Weighted hybrid retrieval
* Reciprocal Rank Fusion (RRF)
* Optional cross-encoder reranking

Retrieval performance is evaluated using:

* Recall@5
* Recall@10
* Mean Reciprocal Rank (MRR)
* nDCG@10

## System Architecture

```text
                    ┌─────────────────────┐
                    │   User Question     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Query Processing    │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
        ┌────────────────┐          ┌────────────────┐
        │ BM25 Retrieval │          │ Dense Retrieval│
        │   (Lexical)    │          │  (E5 + FAISS) │
        └───────┬────────┘          └────────┬───────┘
                │                            │
                └────────────┬───────────────┘
                             ▼
                   ┌─────────────────────┐
                   │ Hybrid / RRF Fusion │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Optional Reranking  │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Retrieved Context   │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ LLM Generation      │
                   │     Qwen3-4B        │
                   └─────────────────────┘
```

## Languages

| Language  | Evaluation Questions |
| --------- | -------------------: |
| English   |                   20 |
| Sinhala   |                   20 |
| Tamil     |                   20 |
| **Total** |               **60** |

The evaluation benchmark contains **60 questions**, distributed equally across the three languages.

## Retrieval Benchmark

The main benchmark compares BM25, multilingual dense retrieval, Reciprocal Rank Fusion, and weighted hybrid retrieval.

| Method        |   Recall@5 |  Recall@10 |        MRR |    nDCG@10 |
| ------------- | ---------: | ---------: | ---------: | ---------: |
| BM25          |     0.9167 |     0.9667 |     0.8466 |     0.8755 |
| Dense E5      |     0.8167 |     0.8333 |     0.5372 |     0.6090 |
| E5 + RRF      |     0.8833 |     0.9667 |     0.7382 |     0.7932 |
| Hybrid α=0.50 | **0.9667** | **0.9667** | **0.8583** | **0.8867** |

### Main Finding

The **weighted hybrid configuration with α = 0.50 produced the strongest overall ranking quality** among the tested configurations.

It achieved:

* Recall@5: **0.9667**
* Recall@10: **0.9667**
* MRR: **0.8583**
* nDCG@10: **0.8867**

The result suggests that combining lexical BM25 signals with multilingual dense retrieval can provide a more robust ranking than relying on dense retrieval alone.

BM25 remained highly competitive, while dense retrieval alone showed substantially lower MRR and nDCG on this controlled benchmark.

## Hybrid Retrieval Experiment

The weighted hybrid retriever combines normalized BM25 and dense retrieval scores:

```text
Hybrid Score =
(1 − α) × BM25 + α × Dense
```

Different α values were evaluated to investigate the contribution of lexical and semantic retrieval.

|    α | Interpretation        |
| ---: | --------------------- |
| 0.00 | BM25 only             |
| 0.25 | BM25-dominant hybrid  |
| 0.50 | Balanced hybrid       |
| 0.75 | Dense-dominant hybrid |
| 1.00 | Dense only            |

The best tested configuration was:

**α = 0.50**

This configuration achieved:

* Recall@5: **0.9667**
* Recall@10: **0.9667**
* MRR: **0.8583**
* nDCG@10: **0.8867**

This experiment provides evidence that the two retrieval approaches contain complementary information.

## Reciprocal Rank Fusion

Reciprocal Rank Fusion (RRF) was evaluated as an alternative rank-based fusion strategy.

The tested RRF configuration achieved:

* Recall@5: **0.8833**
* Recall@10: **0.9667**
* MRR: **0.7382**
* nDCG@10: **0.7932**

Although RRF successfully combined retrieval rankings, it did not outperform the best weighted hybrid configuration on this benchmark.

Therefore, the project reports the **α=0.50 weighted hybrid** as the strongest tested configuration rather than selecting RRF simply because it is a common fusion technique.

## Language-Specific Analysis

The experiments also examined differences between English, Sinhala, and Tamil retrieval.

### English

English queries generally benefited from both lexical and semantic retrieval signals.

The controlled benchmark was used to compare how ranking behaviour changed between BM25, dense, and hybrid retrieval.

### Sinhala

Sinhala was an important retrieval challenge.

Dense retrieval showed weaker ranking behaviour than BM25 on the controlled benchmark, while hybrid retrieval benefited from combining lexical and semantic signals.

This highlights the importance of evaluating multilingual retrieval separately by language rather than relying only on an aggregate score.

### Tamil

Tamil retrieval also showed strong lexical retrieval behaviour in several evaluated cases.

The failure analysis included Tamil queries where BM25 and dense retrieval produced noticeably different rankings, demonstrating that the retrieval methods captured different signals.

## Retrieval Failure Analysis

A dedicated failure-analysis experiment was conducted over the 60-question benchmark.

The analysis identified **23 notable retrieval cases**, including:

* BM25-only ranking advantages
* BM25 vs. dense ranking differences
* Sinhala queries where BM25 ranked the relevant chunk highly while dense retrieval ranked it substantially lower
* Tamil queries where lexical matching provided useful ranking signals

For example, several Sinhala queries showed a relevant chunk ranked near the top by BM25 but considerably lower by dense retrieval.

These cases support the motivation for investigating hybrid retrieval rather than assuming that semantic embeddings will always outperform lexical retrieval.

## Reranking Experiment

A multilingual cross-encoder reranker was also investigated using:

```text
cross-encoder/mmarco-mMiniLMv2-L12-H384-v1
```

The reranking experiment did not consistently improve retrieval performance on the tested configuration.

This was treated as a useful **negative/limited experiment** rather than selecting a more complex model simply because it was expected to perform better.

The result demonstrates an important research principle: additional model complexity should be supported by measured improvement.

## Generation Experiment

The project also integrates **Qwen3-4B through Ollama** for local answer generation.

Generation evaluation was conducted as a preliminary experiment using:

* Token F1
* Context word support
* Citation grounding
* Retrieval latency
* Generation latency

The generation experiment was conducted on a **12-question exploratory subset**, rather than being treated as a full 60-question generation benchmark.

The results varied substantially between questions, including occasional incomplete responses and reasoning-text leakage.

Therefore, generation metrics are treated as **preliminary evidence**, while retrieval metrics form the primary evaluation of the research project.

## Evaluation Data

The project contains:

```text
data/
├── documents/
│   ├── academic_calendar.txt
│   ├── course_module_handbook.txt
│   ├── examination_regulations.txt
│   ├── faculty_handbook.txt
│   ├── institutional_services_guide.txt
│   ├── library_regulations.txt
│   ├── research_innovation_policy.txt
│   ├── scholarship_student_support.txt
│   └── university_student_handbook.txt
│
├── evaluation/
│   ├── evaluation.baseline.jsonl
│   ├── evaluation.enriched.jsonl
│   └── evaluation.example.jsonl
│
└── results/
    ├── failure_analysis.json
    ├── generation_evaluation.json
    └── retrieval_benchmark.json
```

The document corpus is a **synthetic research corpus** created for controlled experimentation.

The evaluation dataset contains 60 questions:

* 20 English
* 20 Sinhala
* 20 Tamil

The benchmark was designed to allow controlled comparison of retrieval methods and analysis of language-specific behaviour.

## Project Structure

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
│   ├── evaluate_generation.py
│   ├── failure_analysis.py
│   ├── ingest.py
│   ├── run_experiments.py
│   ├── run_full_research.py
│   └── validate_evaluation.py
│
├── tests/
│   ├── test_metrics.py
│   └── test_retrieval_logic.py
│
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Shapthana/Initial-release-multilingual-RAG-QA-syste.git
cd Initial-release-multilingual-RAG-QA-syste
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## Build the Retrieval Index

From the backend directory:

```powershell
cd backend
python scripts\ingest.py
```

This prepares the document chunks and retrieval index used by the evaluation pipeline.

## Run Retrieval Evaluation

Validate the evaluation data:

```powershell
python scripts\validate_evaluation.py
```

Run the benchmark:

```powershell
python scripts\evaluate.py
```

## Run Research Experiments

The project also includes scripts for running retrieval experiments:

```powershell
python scripts\run_experiments.py
```

For the complete research workflow:

```powershell
python scripts\run_full_research.py
```

## Run Tests

Install pytest if it is not already installed:

```powershell
pip install pytest
```

Then run:

```powershell
python -m pytest -q
```

## Generation

The project can use Ollama for local LLM generation.

The tested model was:

```text
Qwen3-4B
```

Generation experiments can be run using:

```powershell
python scripts\evaluate_generation.py
```

Generation evaluation is intentionally treated as exploratory because the current experiment uses a smaller subset than the primary retrieval benchmark.

## Research Limitations

The current evaluation has several limitations:

1. The benchmark contains 60 questions and is relatively small.
2. The document corpus is synthetic and controlled rather than a large real-world collection.
3. Sinhala and Tamil retrieval require further investigation on larger and more diverse datasets.
4. Generation evaluation is preliminary and was performed on a smaller exploratory subset.
5. Cross-encoder reranking did not consistently improve the tested configuration.
6. The current benchmark does not establish generalisation to large-scale real-world document collections.

These limitations are important because the reported results should be interpreted as evidence from a controlled research experiment rather than as a universal ranking of retrieval methods.

## Future Work

Future experiments could investigate:

* Larger multilingual document collections
* More Sinhala and Tamil evaluation questions
* Human evaluation of answer faithfulness and correctness
* Stronger multilingual embedding models
* Alternative reranking models
* Query expansion
* Language-specific retrieval strategies
* More robust citation evaluation
* Larger-scale latency and memory benchmarking
* Evaluation on real-world multilingual documents

## Research Takeaway

The experiments show that multilingual RAG retrieval should not be evaluated using a single retrieval method or a single aggregate metric.

In this controlled benchmark, **BM25 and dense retrieval exhibited different strengths**, with BM25 remaining highly competitive and dense retrieval showing weaker ranking quality when used alone.

The **α=0.50 weighted hybrid configuration achieved the strongest overall retrieval performance among the tested configurations**, demonstrating the potential value of combining lexical and semantic signals.

The language-specific analysis also showed why multilingual retrieval should be examined beyond aggregate metrics, particularly for Sinhala and Tamil queries.

The project therefore treats retrieval as an independently measurable research problem within a RAG pipeline rather than evaluating the system only through generated answers.

## Technologies

* Python
* FastAPI
* BM25
* FAISS
* Sentence Transformers
* E5 embeddings
* Multilingual NLP
* Cross-encoder reranking
* Reciprocal Rank Fusion
* Ollama
* Qwen3-4B
* NumPy
* scikit-learn
* Pytest

## Author

**Shapthana Jeganathan**

Computer Engineering Undergraduate
University of Jaffna

GitHub:

https://github.com/Shapthana/Initial-release-multilingual-RAG-QA-syste
