# matcher/clause_matcher.py
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def match_clauses(query_emb, chunk_embs):
    similarities = cosine_similarity([query_emb], chunk_embs)[0]
    ranked = np.argsort(similarities)[::-1]
    return ranked, similarities
