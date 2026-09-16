import math
import re
from collections import Counter


def recall_at_k(retrieved_ids,relevant_ids,k):
    relevant=set(relevant_ids); retrieved=set(retrieved_ids[:k])
    return len(retrieved & relevant)/len(relevant) if relevant else 0.0

def reciprocal_rank(retrieved_ids,relevant_ids):
    relevant=set(relevant_ids)
    for rank,did in enumerate(retrieved_ids,1):
        if did in relevant: return 1.0/rank
    return 0.0

def ndcg_at_k(retrieved_ids,relevant_ids,k):
    relevant=set(relevant_ids)
    dcg=sum(1/math.log2(rank+1) for rank,did in enumerate(retrieved_ids[:k],1) if did in relevant)
    ideal=min(k,len(relevant))
    idcg=sum(1/math.log2(rank+1) for rank in range(1,ideal+1))
    return dcg/idcg if idcg else 0.0

def token_f1(prediction,reference):
    tok=lambda s: re.findall(r"\w+", (s or "").lower(), flags=re.UNICODE)
    p=Counter(tok(prediction)); r=Counter(tok(reference))
    common=sum((p&r).values())
    if not common: return 0.0
    precision=common/max(1,sum(p.values())); recall=common/max(1,sum(r.values()))
    return 2*precision*recall/(precision+recall)
