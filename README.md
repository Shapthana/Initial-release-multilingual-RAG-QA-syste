# Multilingual RAG-Based Document Question Answering & Evaluation System

A research-oriented Retrieval-Augmented Generation (RAG) system for multilingual document question answering across **English, Sinhala, and Tamil**.

The project investigates **retrieval quality, multilingual robustness, controlled experimentation, and systematic evaluation** within a RAG pipeline. The primary focus is retrieval evaluation rather than treating generated-answer quality as the only measure of RAG performance.

## Research Objective

The main research question is:

> How do lexical, dense, and hybrid retrieval methods compare for multilingual document question answering across English, Sinhala, and Tamil?

The system evaluates:

* BM25 lexical retrieval
* Multilingual dense retrieval using E5 embeddings
* Weighted hybrid retrieval
* Reciprocal Rank Fusion (RRF)
* Optional multilingual cross-encoder reranking

Retrieval performance is evaluated using:

* Recall@5
* Recall@10
* Mean Reciprocal Rank (MRR)
* nDCG@10

The experiments also investigate **language-specific retrieval behaviour and retrieval failures**.

---

## System Architecture

```text
                         User Question
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Query Processing   │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
        ┌────────────────┐          ┌────────────────┐
        │ BM25 Retrieval │          │ Dense Retrieval│
        │    Lexical     │          │  E5 + FAISS   │
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
                   │   Qwen3-4B / LLM    │
                   │     Generation      │
                   └─────────────────────┘
```

---

## Multilingual Benchmark

The controlled evaluation benchmark contains **60 questions**, equally distributed across the three languages.

| Language  | Questions |
| --------- | --------: |
| English   |        20 |
| Sinhala   |        20 |
| Tamil     |        20 |
| **Total** |    **60** |

The benchmark was designed to compare retrieval methods under the same evaluation conditions and to investigate language-specific differences.

---

## Retrieval Benchmark

The primary benchmark compares BM25, dense E5 retrieval, RRF, and weighted hybrid retrieval.

| Method            |   Recall@5 |  Recall@10 |        MRR |    nDCG@10 |
| ----------------- | ---------: | ---------: | ---------: | ---------: |
| BM25              |     0.9167 |     0.9667 |     0.8466 |     0.8755 |
| Dense E5          |     0.8167 |     0.8333 |     0.5372 |     0.6090 |
| E5 + RRF          |     0.8833 |     0.9667 |     0.7382 |     0.7932 |
| **Hybrid α=0.50** | **0.9667** | **0.9667** | **0.8583** | **0.8867** |

### Main Finding

The **weighted hybrid configuration with α = 0.50 achieved the strongest overall retrieval performance** among the tested configurations.

Results:

* **Recall@5:** 0.9667
* **Recall@10:** 0.9667
* **MRR:** 0.8583
* **nDCG@10:** 0.8867

The experiment shows that combining lexical and semantic retrieval signals can improve ranking quality compared with using dense retrieval alone.

An important finding was that **BM25 remained highly competitive**, while dense retrieval alone showed substantially lower MRR and nDCG on this controlled multilingual benchmark.

---

## Hybrid Retrieval Experiment

The weighted hybrid retriever combines normalized BM25 and dense retrieval scores:

```text
Hybrid Score =
(1 − α) × BM25 + α × Dense
```

The following α values were investigated:

|        α | Configuration         |
| -------: | --------------------- |
|     0.00 | BM25 only             |
|     0.25 | BM25-dominant hybrid  |
| **0.50** | **Balanced hybrid**   |
|     0.75 | Dense-dominant hybrid |
|     1.00 | Dense only            |

The strongest tested configuration was:

**α = 0.50**

with:

* Recall@5: **0.9667**
* Recall@10: **0.9667**
* MRR: **0.8583**
* nDCG@10: **0.8867**

This result supports the hypothesis that lexical and semantic retrieval provide complementary signals for multilingual question answering.

---

## Reciprocal Rank Fusion

Reciprocal Rank Fusion (RRF) was evaluated as a rank-based alternative to weighted score fusion.

The tested RRF configuration achieved:

* Recall@5: **0.8833**
* Recall@10: **0.9667**
* MRR: **0.7382**
* nDCG@10: **0.7932**

RRF provided a useful comparison, but it did **not** outperform the best weighted hybrid configuration in this benchmark.

This is reported as an experimental finding rather than assuming that a commonly used fusion method must perform best.

---

## Language-Specific Analysis

The benchmark was also analysed by language to identify retrieval behaviour that can be hidden by aggregate metrics.

### English

English queries generally benefited from both lexical and semantic retrieval signals.

The experiments were used to compare how BM25, dense retrieval, and hybrid retrieval changed the ranking of relevant document chunks.

### Sinhala

Sinhala represented an important retrieval challenge.

Dense retrieval showed weaker ranking behaviour than BM25 in the controlled benchmark. Several Sinhala queries demonstrated cases where BM25 ranked the relevant chunk highly while dense retrieval ranked it considerably lower.

This suggests that lexical matching can provide useful signals for Sinhala queries that are not consistently captured by multilingual dense embeddings.

### Tamil

Tamil retrieval also showed strong lexical retrieval behaviour in several evaluated cases.

The failure analysis identified Tamil queries where BM25 and dense retrieval produced substantially different rankings, demonstrating that the two retrieval methods captured different signals.

---

## Retrieval Failure Analysis

A dedicated failure-analysis experiment was conducted over the **60-question benchmark**.

The analysis identified **23 notable retrieval cases**, including:

* BM25-only ranking advantages
* BM25 vs. dense ranking differences
* Sinhala queries where BM25 ranked relevant content highly while dense retrieval ranked it lower
* Tamil queries showing different lexical and semantic ranking behaviour

The failure analysis was used to understand **why** aggregate retrieval metrics differed rather than reporting only final scores.

A key observation was that dense retrieval did not consistently outperform lexical retrieval for Sinhala queries, supporting the investigation of hybrid retrieval.

---

## Reranking Experiment

An optional multilingual cross-encoder reranker was investigated using:

```text
cross-encoder/mmarco-mMiniLMv2-L12-H384-v1
```

The reranking experiment did **not consistently improve retrieval performance** on the tested configuration.

Rather than selecting a more complex model simply because it was expected to perform better, the experiment was retained as a **negative/limited result**.

This provides evidence for an important research principle:

> Additional model complexity should be supported by measured improvement.

---

## Generation Experiment

The system integrates **Qwen3-4B through Ollama** for local answer generation.

Generation was evaluated using:

* Token F1
* Context word support
* Citation grounding
* Retrieval latency
* Generation latency

Generation evaluation was conducted on a **12-question exploratory subset**.

The experiment showed substantial variation between questions, including occasional incomplete responses and reasoning-text leakage.

Therefore, generation results are treated as **preliminary evidence**, while the 60-question retrieval benchmark remains the primary evaluation of the research project.

---

## Evaluation Data

The project contains a controlled synthetic document corpus and multilingual evaluation dataset.

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

The document corpus is a **synthetic research corpus created for controlled experimentation**.

The evaluation benchmark contains:

* 20 English questions
* 20 Sinhala questions
* 20 Tamil questions

---

## Project Structure

The repository is organized at the project root as follows:
```text
Initial-release-multilingual-RAG-QA-syste/
├── app/                  # Application source modules
├── backend/              # Backend runtime and service scripts
├── data/                 # Documents, evaluation data, indexes and results
├── docs/                 # Research and project documentation
├── experiments/          # Retrieval and evaluation experiments
├── frontend/             # Frontend application
├── scripts/              # Supporting scripts
├── tests/                # Automated tests
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── .gitignore
```

---

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

From the repository root:

```powershell
pip install -r requirements.txt
```

### 4. Enter the backend directory

```powershell
cd backend
```

---

## Build the Retrieval Index

From the `backend` directory:

```powershell
python scripts\ingest.py
```

This prepares the document chunks and retrieval index used by the evaluation pipeline.


## Validate Evaluation Data

From the `backend` directory:

```powershell
python scripts\validate_evaluation.py
```

---

## Run Retrieval Evaluation

```powershell
python scripts\evaluate.py
```

The evaluation reports retrieval metrics including Recall@5, Recall@10, MRR, and nDCG@10.

---

## Run Research Experiments

To run the retrieval experiments:

```powershell
python scripts\run_experiments.py
```

For the complete research workflow:

```powershell
python scripts\run_full_research.py
```

---

## Run Tests

Install pytest if necessary:

```powershell
pip install pytest
```

Then:

```powershell
python -m pytest -q
```

---

## Local Generation

The project supports local LLM generation using Ollama.

The tested model was:

```text
Qwen3-4B
```

Generation evaluation can be run with:

```powershell
python scripts\evaluate_generation.py
```

The generation experiment is exploratory and should not be interpreted as a full 60-question generation benchmark.

---

## Research Limitations

The current study has several limitations:

1. The benchmark contains 60 questions and is relatively small.
2. The document corpus is synthetic and controlled rather than a large real-world collection.
3. Sinhala and Tamil retrieval require further investigation using larger and more diverse datasets.
4. Generation evaluation is preliminary and uses a smaller exploratory subset.
5. Cross-encoder reranking did not consistently improve the tested configuration.
6. The current benchmark does not establish generalisation to large-scale real-world multilingual collections.

The reported results should therefore be interpreted as findings from a **controlled research experiment**, not as a universal ranking of retrieval methods.

---

## Future Work

Future experiments could investigate:

* Larger multilingual document collections
* More Sinhala and Tamil evaluation questions
* Stronger multilingual embedding models
* Alternative reranking models
* Query expansion
* Language-specific retrieval strategies
* Human evaluation of answer faithfulness and correctness
* More robust citation evaluation
* Larger-scale latency and memory benchmarking
* Evaluation on real-world multilingual documents

---

## Research Takeaway

The experiments demonstrate that multilingual RAG retrieval should not be evaluated using a single retrieval method or a single aggregate metric.

In this controlled benchmark:

* **BM25 remained highly competitive**
* **Dense retrieval alone showed weaker ranking quality**
* **Lexical and semantic retrieval exhibited complementary behaviour**
* **Hybrid α=0.50 achieved the strongest overall retrieval performance**
* **Sinhala highlighted an important weakness of dense retrieval**
* **Failure analysis revealed meaningful ranking differences between retrieval methods**

The project therefore treats retrieval as an independently measurable research problem within a RAG pipeline, using controlled experiments, quantitative metrics, language-specific analysis, and failure analysis.

---

## Technologies

* Python
* FastAPI
* BM25
* FAISS
* Sentence Transformers
* E5 embeddings
* Multilingual NLP
* Reciprocal Rank Fusion
* Cross-encoder reranking
* Ollama
* Qwen3-4B
* NumPy
* scikit-learn
* Pytest

---

## Author

**Shapthana Jeganathan**

Computer Engineering Undergraduate
University of Jaffna

GitHub repository:
https://github.com/Shapthana/Initial-release-multilingual-RAG-QA-syste
