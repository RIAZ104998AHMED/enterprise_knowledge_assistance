# rag/retrieve.py
import pickle
import numpy as np
import faiss
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from config import settings

# Load the vector store and chunks
DOC_CHUNKS_PATH = "rag/doc_chunks.pkl"
VECTOR_STORE_PATH = "rag/vector_store.faiss"

with open(DOC_CHUNKS_PATH, "rb") as f:
    chunks = pickle.load(f)

index = faiss.read_index(VECTOR_STORE_PATH)

# Initialize BM25 sparse index
corpus = [c["text"].split() for c in chunks]
bm25 = BM25Okapi(corpus)

# Dense embedding model
model = SentenceTransformer(settings.EMBEDDING_MODEL)

def hybrid_retrieve(query, top_k=settings.TOP_K, alpha=0.5):
    """
    Hybrid retrieval: dense embedding + BM25 sparse retrieval + RRF fusion.
    Args:
        query (str): User question
        top_k (int): Number of results to return
        alpha (float): Weighting factor for fusion (currently not used, can extend)
    Returns:
        List of top_k candidate chunks (dict with id, text, score)
    """
    # Dense embedding retrieval
    q_emb = model.encode([query])
    D, I = index.search(q_emb, top_k * 2)  # retrieve more to allow rerank
    dense_results = [{"id": chunks[i]["id"], "text": chunks[i]["text"], "score": float(D[0][j])}
                     for j, i in enumerate(I[0])]

    # Sparse BM25 retrieval
    bm25_scores = bm25.get_scores(query.split())
    top_indices = np.argsort(bm25_scores)[-top_k * 2:]  # top candidates
    sparse_results = [{"id": chunks[i]["id"], "text": chunks[i]["text"], "score": float(bm25_scores[i])}
                      for i in top_indices]

    # Reciprocal Rank Fusion (RRF)
    id_to_score = {}
    for r in dense_results + sparse_results:
        score = r["score"]
        id_to_score[r["id"]] = id_to_score.get(r["id"], 0) + (1.0 / (score + 1e-6))  # avoid div0

    # Merge dense results using RRF
    for r in dense_results:
        r["rrf_score"] = id_to_score[r["id"]]

    top_results = sorted(dense_results, key=lambda x: x["rrf_score"], reverse=True)[:top_k]
    return top_results

if __name__ == "__main__":
    # Simple test
    query = input("Enter a test query: ")
    results = hybrid_retrieve(query)
    for r in results:
        print(f"Chunk ID: {r['id']}, Score: {r['rrf_score']:.4f}")
        print(r['text'][:200], "...\n")