from sklearn.metrics.pairwise import cosine_similarity


def computeCosineSimilarity(va, vb):
    dot = sum(a * b for a, b in zip(va, vb))
    norm_a = sum(a * a for a in va) ** 0.5
    norm_b = sum(b * b for b in vb) ** 0.5
    if norm_a > 0 and norm_b > 0:
        # Cosine similarity
        cos_sim = dot / float((norm_a * norm_b))
    else:
        cos_sim = 0
    return float(cos_sim)
