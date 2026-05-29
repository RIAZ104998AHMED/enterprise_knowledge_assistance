# agents/retriever_agent.py
from agents.schemas import RetrievalRequest, RetrievalResult
from rag.retrieve import hybrid_retrieve
from rag.reranking import rerank
from config import settings

class RetrieverAgent:
    """
    Retrieves top candidate chunks for a query using hybrid retrieval + reranking.
    """

    def handle(self, request: RetrievalRequest) -> RetrievalResult:
        # Step 1: Hybrid retrieval
        candidates = hybrid_retrieve(request.query, top_k=request.top_k)

        # Step 2: Optional reranking
        reranked = rerank(request.query, candidates)

        # Return as RetrievalResult schema
        return RetrievalResult(chunks=reranked)

if __name__ == "__main__":
    # Simple test
    from agents.schemas import RetrievalRequest
    agent = RetrieverAgent()
    req = RetrievalRequest(query="Who founded Google?", top_k=3)
    result = agent.handle(req)
    for c in result.chunks:
        print(c["id"], c["text"][:100], "...")