from app.services.evaluator import recall_at_k, reciprocal_rank, ndcg_at_k

def test_recall():
    assert recall_at_k(["a","b","c"], ["b"], 2) == 1.0

def test_mrr():
    assert reciprocal_rank(["x","b"], ["b"]) == 0.5

def test_ndcg():
    assert ndcg_at_k(["b","x"], ["b"], 2) == 1.0
