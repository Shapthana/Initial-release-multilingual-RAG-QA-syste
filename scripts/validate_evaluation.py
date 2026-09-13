from pathlib import Path
import json
import sys

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

ROOT = Path(__file__).resolve().parents[1]

EVAL_FILE = (
    ROOT
    / "data"
    / "evaluation"
    / "evaluation.example.jsonl"
)

METADATA_FILE = ROOT / "data" / "index" / "metadata.json"


def load_jsonl(path):
    rows = []

    with path.open(
        "r",
        encoding="utf-8-sig"
    ) as f:

        for line_number, line in enumerate(
            f,
            start=1
        ):
            line = line.strip()

            if not line:
                continue

            try:
                rows.append(
                    json.loads(line)
                )
            except json.JSONDecodeError as e:
                print(
                    f"ERROR: Invalid JSON at "
                    f"line {line_number}: {e}"
                )

    return rows


def load_metadata(path):
    data = json.loads(
        path.read_text(
            encoding="utf-8-sig"
        )
    )

    return {
        item["id"]: item
        for item in data
    }


def validate_questions(rows, documents):

    errors = []
    warnings = []

    seen_ids = set()

    for row_number, row in enumerate(
        rows,
        start=1
    ):

        required_fields = [
            "id",
            "language",
            "question",
            "answer",
            "source",
            "relevant_chunk_ids"
        ]

        for field in required_fields:

            if field not in row:
                errors.append(
                    f"Row {row_number}: "
                    f"missing field '{field}'"
                )

        question_id = row.get("id")

        if question_id in seen_ids:
            errors.append(
                f"Duplicate question ID: "
                f"{question_id}"
            )

        seen_ids.add(question_id)

        language = row.get(
            "language"
        )

        if language not in {
            "en",
            "si",
            "ta"
        }:
            errors.append(
                f"{question_id}: "
                f"invalid language '{language}'"
            )

        relevant_ids = row.get(
            "relevant_chunk_ids",
            []
        )

        if not relevant_ids:
            errors.append(
                f"{question_id}: "
                f"no relevant chunks"
            )

        for chunk_id in relevant_ids:

            if chunk_id not in documents:
                errors.append(
                    f"{question_id}: "
                    f"chunk '{chunk_id}' "
                    f"does not exist"
                )

    return errors, warnings


def print_summary(rows):

    language_counts = {}

    for row in rows:

        language = row["language"]

        language_counts[language] = (
            language_counts.get(
                language,
                0
            ) + 1
        )

    print()
    print("=" * 70)
    print("EVALUATION DATASET SUMMARY")
    print("=" * 70)

    print(
        f"Total questions: {len(rows)}"
    )

    print()

    for language in [
        "en",
        "si",
        "ta"
    ]:

        print(
            f"{language}: "
            f"{language_counts.get(language, 0)}"
        )


def main():

    print("=" * 70)
    print("VALIDATING EVALUATION DATASET")
    print("=" * 70)

    if not EVAL_FILE.exists():

        print(
            f"ERROR: Evaluation file not found:\n"
            f"{EVAL_FILE}"
        )

        return

    if not METADATA_FILE.exists():

        print(
            f"ERROR: Metadata file not found:\n"
            f"{METADATA_FILE}"
        )

        return

    rows = load_jsonl(
        EVAL_FILE
    )

    documents = load_metadata(
        METADATA_FILE
    )

    print(
        f"Loaded questions: {len(rows)}"
    )

    print(
        f"Loaded chunks: {len(documents)}"
    )

    errors, warnings = validate_questions(
        rows,
        documents
    )

    print_summary(rows)

    print()

    if errors:

        print("=" * 70)
        print("ERRORS")
        print("=" * 70)

        for error in errors:
            print(
                f"[ERROR] {error}"
            )

        print()
        print(
            f"Total errors: {len(errors)}"
        )

        return

    print("=" * 70)
    print("VALIDATION PASSED")
    print("=" * 70)

    print(
        "All question IDs are unique."
    )

    print(
        "All required fields are present."
    )

    print(
        "All relevant chunk IDs exist."
    )


if __name__ == "__main__":
    main()
