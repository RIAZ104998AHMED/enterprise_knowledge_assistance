# agents/reviewer_agent.py
from agents.schemas import SafetyVerdict
from safety.output_guards import grounding_check, redact_pii

class ReviewerAgent:
    """
    Evaluates the synthesized draft for safety:
    - Grounding check
    - PII redaction
    """

    def handle(self, draft, retrieved_chunks):
        """
        Args:
            draft (dict): {"answer": str, "citations": List[str]}
            retrieved_chunks (list): list of dicts from retriever
        Returns:
            SafetyVerdict: approved=True/False, notes, optional redacted_draft
        """
        missing = grounding_check(draft, retrieved_chunks)
        if missing:
            return SafetyVerdict(approved=False, notes=f"Missing citations: {missing}", redacted_draft=None)

        # Redact any PII from answer
        draft["answer"] = redact_pii(draft["answer"])

        return SafetyVerdict(approved=True, notes="Approved", redacted_draft=None)

if __name__ == "__main__":
    # Test
    mock_draft = {
        "answer": "Contact john.doe@example.com for details.",
        "citations": ["chunk_0"]
    }
    mock_chunks = [{"id": "chunk_0", "text": "Passwords must be rotated every 90 days."}]
    agent = ReviewerAgent()
    verdict = agent.handle(mock_draft, mock_chunks)
    print(verdict)