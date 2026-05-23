# rag/reranking.py
from sentence_transformers import CrossEncoder
from config import settings

# Load cross-encoder for re-ranking
# You can replace with any cross-encoder from Hugging Face
reranker_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query, candidates, top_n=settings.RERANK_TOP_N):
    """
    Re-rank candidate chunks based on semantic similarity with query.

    Args:
        query (str): User question
        candidates (list): List of candidate dicts with keys 'id' and 'text'
        top_n (int): Number of top candidates to return after reranking

    Returns:
        List of dicts: top_n candidates with additional key 'rerank_score'
    """
    if not candidates:
        return []

    # Prepare input pairs for cross-encoder
    pairs = [[query, c["text"]] for c in candidates]

    # Compute rerank scores
    scores = reranker_model.predict(pairs)

    # Assign rerank scores
    for i, c in enumerate(candidates):
        c["rerank_score"] = float(scores[i])

    # Sort candidates by rerank score
    candidates_sorted = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)

    return candidates_sorted[:top_n]

if __name__ == "__main__":
    # Simple test
    sample_candidates = [
        {"id": "0_0", "text": "Passwords must be rotated every 90 days."},
        {"id": "0_1", "text": "MFA is required for all privileged accounts."},
        {"id": "0_2", "text": "Accounts are locked after 5 failed login attempts."}
    ]
    query = "What is the company password policy?"
    top_candidates = rerank(query, sample_candidates)
    for c in top_candidates:
        print(f"ID: {c['id']}, Score: {c['rerank_score']:.4f}")
        print(c["text"])