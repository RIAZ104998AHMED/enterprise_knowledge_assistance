# agents/orchestrator.py
from agents.retriever_agent import RetrieverAgent
from agents.synthesizer_agent import SynthesizerAgent
from agents.reviewer_agent import ReviewerAgent
from agents.schemas import RetrievalRequest, SynthesisRequest
from config import settings

MAX_ROUNDS = 3  # maximum retry loop for safety feedback

class Orchestrator:
    def __init__(self):
        self.retriever = RetrieverAgent()
        self.synthesizer = SynthesizerAgent()
        self.reviewer = ReviewerAgent()

    def handle_query(self, query, role="intern"):
        """
        Full orchestrator workflow:
        1. Retrieve candidate chunks
        2. Synthesize answer
        3. Safety review (feedback loop up to MAX_ROUNDS)
        """
        ret_req = RetrievalRequest(query=query, role=role, top_k=settings.TOP_K)
        retrieved = self.retriever.handle(ret_req)

        synth_req = SynthesisRequest(query=query, retrieved_chunks=retrieved.chunks, role=role)

        round_counter = 0
        while round_counter < MAX_ROUNDS:
            round_counter += 1

            # Generate draft answer
            draft = self.synthesizer.handle(synth_req)

            # Run safety review
            verdict = self.reviewer.handle(draft, retrieved.chunks)

            if verdict.approved:
                # Approved draft
                return draft, verdict
            else:
                # Feedback loop: re-dispatch to synthesizer
                # Optionally modify synth_req based on verdict.notes
                synth_req.retrieved_chunks = retrieved.chunks  # could adjust in advanced implementation

        # If max rounds exceeded without approval, return last draft with verdict
        return draft, verdict

if __name__ == "__main__":
    # Quick test
    orchestrator = Orchestrator()
    query = "What is the company password rotation policy?"
    draft, verdict = orchestrator.handle_query(query)
    print("Answer:", draft["answer"])
    print("Citations:", draft.get("citations", []))
    print("Safety approved:", verdict.approved, "Notes:", verdict.notes)