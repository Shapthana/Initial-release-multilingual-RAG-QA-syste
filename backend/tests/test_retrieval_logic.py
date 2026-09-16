import pytest

pytest.importorskip("rank_bm25")
pytest.importorskip("sentence_transformers")

from app.services.retrieval import HybridRetriever


def test_minmax():
    assert HybridRetriever._minmax([1.0, 2.0, 3.0]) == [0.0, 0.5, 1.0]
    assert HybridRetriever._minmax([2.0, 2.0]) == [1.0, 1.0]
