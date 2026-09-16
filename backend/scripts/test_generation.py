
from pathlib import Path
import sys
import time

# Add backend directory to Python path
sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from app.services.generator import generate_answer


# ------------------------------------------------------------
# Test context
# ------------------------------------------------------------

contexts = [
    {
        "source": "test-document",
        "text": (
            "A university is an institution that provides "
            "higher education, research opportunities, "
            "and degree programs."
        ),
    }
]


# ------------------------------------------------------------
# Test question
# ------------------------------------------------------------

query = "What is a university?"


# ------------------------------------------------------------
# Run project generator
# ------------------------------------------------------------

print("Testing project generator...")
print("Model: qwen3:4b")
print()

start = time.perf_counter()

result = generate_answer(
    query,
    contexts
)

elapsed = time.perf_counter() - start


# ------------------------------------------------------------
# Display result
# ------------------------------------------------------------

print("=" * 60)
print("ANSWER")
print("=" * 60)

print(result["answer"])

print()
print("=" * 60)
print("TIMING")
print("=" * 60)

print(f"Generation time: {elapsed:.2f} seconds")
print(f"Citations: {result['citations']}")
