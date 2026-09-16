from pathlib import Path
import argparse
import json
import re
import requests
import sys
import time

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from app.config import (
    LLM_BASE_URL,
    LLM_API_KEY,
    LLM_MODEL,
)

from app.services.retrieval import HybridRetriever
from app.services.generator import generate_answer
from app.services.evaluator import token_f1


# ============================================================
# Paths
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

EVAL = (
    ROOT
    / "data"
    / "evaluation"
    / "evaluation.example.jsonl"
)


# ============================================================
# Metrics helpers
# ============================================================

def tokens(text):
    return set(
        re.findall(
            r"\w+",
            (text or "").lower(),
            flags=re.UNICODE,
        )
    )


def citation_ids(answer, n):
    """
    Extract valid citation numbers such as [1], [2], etc.
    """

    return [
        int(x)
        for x in re.findall(
            r"\[(\d+)\]",
            answer or "",
        )
        if 1 <= int(x) <= n
    ]


def support_ratio(answer, text):
    """
    Deterministic lexical support proxy.

    Measures the proportion of answer words
    that appear somewhere in the retrieved context.
    """

    words = [
        word
        for word in re.findall(
            r"\w+",
            (answer or "").lower(),
            flags=re.UNICODE,
        )
        if len(word) > 2
    ]

    if not words:
        return 0.0

    context = (text or "").lower()

    supported = sum(
        word in context
        for word in words
    )

    return supported / len(words)


def citation_grounding(answer, contexts):
    """
    Deterministic citation-support proxy.

    For each cited context, calculate how much
    of the answer vocabulary occurs in that source.
    """

    citations = citation_ids(
        answer,
        len(contexts),
    )

    if not citations:
        return 0.0

    answer_words = tokens(answer)

    if not answer_words:
        return 0.0

    scores = []

    for citation_number in citations:

        source_words = tokens(
            contexts[citation_number - 1].get(
                "text",
                "",
            )
        )

        score = (
            len(answer_words & source_words)
            / max(1, len(answer_words))
        )

        scores.append(score)

    return sum(scores) / len(scores)


# ============================================================
# Optional LLM judge
# ============================================================

def llm_judge(
    query,
    answer,
    reference,
    contexts,
    timeout=60,
):
    """
    Optional model-based evaluation.

    Returns scores for:
        correctness
        faithfulness
        citation_correctness
    """

    if not (
        LLM_BASE_URL
        and LLM_MODEL
    ):
        return None

    evidence = "\n\n".join(
        f"[{i + 1}] {context.get('text', '')}"
        for i, context in enumerate(contexts)
    )

    prompt = (
        "Evaluate this grounded multilingual QA answer. "
        "Return ONLY JSON with integer scores 1-5 for "
        "correctness, faithfulness, citation_correctness, "
        "and a short reason.\n\n"

        "Correctness compares with the reference answer. "

        "Faithfulness checks whether claims are supported "
        "by the provided evidence. "

        "Citation correctness checks whether cited evidence "
        "supports the claims.\n\n"

        f"Question: {query}\n"
        f"Reference: {reference}\n"
        f"Answer: {answer}\n"
        f"Evidence:\n{evidence}"
    )

    headers = {
        "Content-Type": "application/json"
    }

    if LLM_API_KEY:
        headers["Authorization"] = (
            f"Bearer {LLM_API_KEY}"
        )

    payload = {
        "model": LLM_MODEL,

        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a strict QA evaluator. "
                    "Output JSON only."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],

        "temperature": 0,
    }

    try:

        response = requests.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=timeout,
        )

        response.raise_for_status()

        text = (
            response
            .json()
            ["choices"][0]
            ["message"]
            ["content"]
        )

        # Find JSON object.
        match = re.search(
            r"\{.*\}",
            text,
            re.S,
        )

        if not match:
            return {
                "judge_parse_error": True,
                "raw": text,
            }

        try:

            return json.loads(
                match.group(0)
            )

        except json.JSONDecodeError:

            return {
                "judge_parse_error": True,
                "raw": text,
            }

    except requests.exceptions.Timeout:

        return {
            "judge_timeout": True,
            "timeout_seconds": timeout,
        }

    except Exception as exc:

        return {
            "judge_error": str(exc),
        }


# ============================================================
# Representative question selection
# ============================================================

def select_representative_questions(rows):
    """
    Select 12 representative questions:

        4 English
        4 Sinhala
        4 Tamil

    Preference:

        factual
        procedural
        list
        temporal

    This keeps language coverage balanced while avoiding
    a large 60-question generation run.
    """

    selected = []

    preferred_types = [
        "factual",
        "procedural",
        "list",
        "temporal",
    ]

    for language in [
        "en",
        "si",
        "ta",
    ]:

        language_rows = [
            row
            for row in rows
            if row.get("language") == language
        ]

        chosen = []

        # ----------------------------------------------------
        # Prefer one question of each question type
        # ----------------------------------------------------

        for question_type in preferred_types:

            matches = [
                row
                for row in language_rows
                if row.get("question_type")
                == question_type
            ]

            if matches:
                chosen.append(
                    matches[0]
                )

        # ----------------------------------------------------
        # Fill remaining slots if necessary
        # ----------------------------------------------------

        for row in language_rows:

            if len(chosen) >= 4:
                break

            if row not in chosen:
                chosen.append(row)

        selected.extend(
            chosen[:4]
        )

    return selected


# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Evaluate multilingual RAG answer generation."
        )
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help=(
            "Evaluate only the first N selected "
            "questions."
        ),
    )

    parser.add_argument(
        "--representative",
        action="store_true",
        help=(
            "Select 12 balanced questions: "
            "4 English, 4 Sinhala, 4 Tamil."
        ),
    )

    parser.add_argument(
        "--llm-judge",
        action="store_true",
        help=(
            "Use Ollama as an additional "
            "model-based evaluator."
        ),
    )

    parser.add_argument(
        "--judge-timeout",
        type=int,
        default=60,
        help=(
            "Timeout in seconds for each "
            "LLM judge request."
        ),
    )

    parser.add_argument(
        "--output",
        default=(
            "data/results/"
            "generation_evaluation.json"
        ),
        help="Output JSON path.",
    )

    args = parser.parse_args()


    # ========================================================
    # Configuration check
    # ========================================================

    if not (
        LLM_BASE_URL
        and LLM_MODEL
    ):

        raise SystemExit(
            "Configure LLM_BASE_URL and "
            "LLM_MODEL before generation evaluation."
        )

    print(
        f"LLM model: {LLM_MODEL}"
    )

    print(
        f"LLM endpoint: {LLM_BASE_URL}"
    )


    # ========================================================
    # Load retriever
    # ========================================================

    retriever = HybridRetriever()

    retriever.load(
        ROOT / "data/index/faiss.index",
        ROOT / "data/index/metadata.json",
    )


    # ========================================================
    # Load evaluation dataset
    # ========================================================

    rows = [
        json.loads(line)
        for line in EVAL.read_text(
            encoding="utf-8-sig"
        ).splitlines()
        if line.strip()
    ]

    print(
        f"Loaded evaluation questions: {len(rows)}"
    )


    # ========================================================
    # Select representative questions
    # ========================================================

    if args.representative:

        rows = select_representative_questions(
            rows
        )

        print(
            "Using representative evaluation: "
            f"{len(rows)} questions"
        )


    # ========================================================
    # Apply limit AFTER representative selection
    # ========================================================

    if args.limit:

        if args.limit < 1:

            raise SystemExit(
                "--limit must be >= 1."
            )

        rows = rows[:args.limit]


    # ========================================================
    # Final selection information
    # ========================================================

    print(
        f"Questions selected: {len(rows)}"
    )

    language_counts = {}

    for row in rows:

        language = row.get(
            "language",
            "unknown",
        )

        language_counts[language] = (
            language_counts.get(
                language,
                0,
            )
            + 1
        )

    print(
        f"Language distribution: "
        f"{language_counts}"
    )

    print()


    # ========================================================
    # Evaluation loop
    # ========================================================

    results = []

    for index, row in enumerate(
        rows,
        start=1,
    ):

        print(
            f"[{index}/{len(rows)}] "
            f"{row['id']} "
            f"({row.get('language', 'unknown')})"
        )


        # ----------------------------------------------------
        # Retrieval timing
        # ----------------------------------------------------

        retrieval_start = (
            time.perf_counter()
        )


        # ----------------------------------------------------
        # RRF retrieval
        #
        # Research configuration:
        #
        # E5 multilingual embeddings
        # +
        # BM25
        # +
        # Reciprocal Rank Fusion
        #
        # Top 5 contexts are passed to the generator.
        # ----------------------------------------------------

        contexts = retriever.rrf_search(
            row["question"],
            5,
        )


        retrieval_ms = (
            time.perf_counter()
            - retrieval_start
        ) * 1000


        # ----------------------------------------------------
        # Generation
        # ----------------------------------------------------

        generation_start = (
            time.perf_counter()
        )

        try:

            generated = generate_answer(
                row["question"],
                contexts,
            )

            answer = generated.get(
                "answer",
                "",
            )

        except Exception as exc:

            print(
                f"  Generation error: {exc}"
            )

            answer = ""


        generation_ms = (
            time.perf_counter()
            - generation_start
        ) * 1000


        # ----------------------------------------------------
        # Calculate metrics
        # ----------------------------------------------------

        item = {

            "id": row["id"],

            "language": row.get(
                "language"
            ),

            "question_type": row.get(
                "question_type"
            ),

            "question": row[
                "question"
            ],

            "reference_answer": row[
                "answer"
            ],

            "answer": answer,

            "answer_token_f1": round(
                token_f1(
                    answer,
                    row["answer"],
                ),
                4,
            ),

            "context_word_support": round(
                support_ratio(
                    answer,
                    " ".join(
                        c.get(
                            "text",
                            "",
                        )
                        for c in contexts
                    ),
                ),
                4,
            ),

            "citation_ids": citation_ids(
                answer,
                len(contexts),
            ),

            "citation_grounding_proxy": round(
                citation_grounding(
                    answer,
                    contexts,
                ),
                4,
            ),

            "retrieval_latency_ms": round(
                retrieval_ms,
                2,
            ),

            "generation_latency_ms": round(
                generation_ms,
                2,
            ),

            "sources": [
                c.get("source")
                for c in contexts
            ],
        }


        # ----------------------------------------------------
        # Optional LLM judge
        # ----------------------------------------------------

        if (
            args.llm_judge
            and answer
        ):

            print(
                "  Running LLM judge..."
            )

            item["llm_judge"] = (
                llm_judge(
                    row["question"],
                    answer,
                    row["answer"],
                    contexts,
                    timeout=args.judge_timeout,
                )
            )


        results.append(item)


        # ----------------------------------------------------
        # Per-question output
        # ----------------------------------------------------

        print(
            f"  F1="
            f"{item['answer_token_f1']:.4f} "
            f"support="
            f"{item['context_word_support']:.4f} "
            f"citation="
            f"{item['citation_grounding_proxy']:.4f}"
        )


    # ========================================================
    # Summary helper
    # ========================================================

    def mean(field):

        values = [
            item[field]
            for item in results
            if isinstance(
                item.get(field),
                (int, float),
            )
        ]

        if not values:
            return None

        return round(
            sum(values)
            / len(values),
            4,
        )


    # ========================================================
    # Summary
    # ========================================================

    summary = {

        "questions": len(results),

        "language_distribution":
            language_counts,

        "retrieval_method":
    "BM25 + E5 + RRF",

        "top_k":
            5,

        "mean_answer_token_f1":
            mean(
                "answer_token_f1"
            ),

        "mean_context_word_support":
            mean(
                "context_word_support"
            ),

        "mean_citation_grounding_proxy":
            mean(
                "citation_grounding_proxy"
            ),

        "mean_retrieval_latency_ms":
            mean(
                "retrieval_latency_ms"
            ),

        "mean_generation_latency_ms":
            mean(
                "generation_latency_ms"
            ),
    }


    # ========================================================
    # Output JSON
    # ========================================================

    output = {

        "summary": summary,

        "evaluation_notes": [

            (
                "This is a small representative "
                "generation evaluation."
            ),

            (
                "The representative evaluation "
                "contains up to 12 questions: "
                "4 English, 4 Sinhala and 4 Tamil."
            ),

            (
                "The --limit option can be used "
                "after representative selection "
                "for debugging or small pilot runs."
            ),

            ("Generation evaluation uses "
"BM25 and E5 multilingual embeddings with "
"Reciprocal Rank Fusion (RRF)."
            ),

            (
                "The top 5 retrieved contexts are "
                "provided to the answer generator."
            ),

            (
                "answer_token_f1 is a lexical "
                "correctness proxy."
            ),

            (
                "context_word_support is a deterministic "
                "grounding proxy."
            ),

            (
                "citation_grounding_proxy is a "
                "deterministic citation-support proxy."
            ),

            (
                "These deterministic metrics are not "
                "human-validated faithfulness measures."
            ),

            (
                "LLM judge scores, when enabled, "
                "are model-based and should be "
                "reported as such."
            ),

            (
                "The benchmark corpus is controlled "
                "and synthetic and should not be "
                "treated as production-scale evidence."
            ),
        ],

        "results": results,
    }


    # ========================================================
    # Save
    # ========================================================

    output_path = (
        ROOT / args.output
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


    # ========================================================
    # Final console summary
    # ========================================================

    print()

    print(
        "=" * 60
    )

    print(
        "GENERATION EVALUATION COMPLETE"
    )

    print(
        "=" * 60
    )

    print(
        f"Questions: {len(results)}"
    )

    print(
    "Retrieval method: BM25 + E5 + RRF"
)

    print(
        "Mean token F1: "
        f"{summary['mean_answer_token_f1']}"
    )

    print(
        "Mean context support: "
        f"{summary['mean_context_word_support']}"
    )

    print(
        "Mean citation grounding: "
        f"{summary['mean_citation_grounding_proxy']}"
    )

    print(
        "Mean retrieval latency: "
        f"{summary['mean_retrieval_latency_ms']} ms"
    )

    print(
        "Mean generation latency: "
        f"{summary['mean_generation_latency_ms']} ms"
    )

    print()

    print(
        f"Saved to: {output_path}"
    )


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()