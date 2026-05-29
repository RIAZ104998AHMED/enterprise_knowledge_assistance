# agents/synthesizer_agent.py
from agents.schemas import SynthesisRequest
from config import settings
from openrouter import OpenRouter

class SynthesizerAgent:
    def __init__(self):
        self.router = OpenRouter(api_key=settings.OPENROUTER_API_KEY)

    def generate_answer(self, prompt):
        response = self.router.completions.create(
            model=settings.SYNTHESIZER_MODEL,
            prompt=prompt,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].text

    def handle(self, request: SynthesisRequest):
        """
        Args:
            request (SynthesisRequest): contains query and retrieved_chunks
        Returns:
            dict: {"answer": str, "citations": List[str]}
        """
        if not request.retrieved_chunks:
            return {"answer": "I don't have enough information.", "citations": []}

        # Simple synthesis: concatenate first 3 chunks
        answer_text = " ".join([c["text"] for c in request.retrieved_chunks[:3]])
        citations = [c["id"] for c in request.retrieved_chunks[:3]]
        return {"answer": answer_text, "citations": citations}

if __name__ == "__main__":
    # Test
    agent = SynthesizerAgent()
    mock_chunks = [
        {"id": "0_0", "text": "Passwords must be rotated every 90 days."},
        {"id": "0_1", "text": "MFA is required for all privileged accounts."},
        {"id": "0_2", "text": "Accounts are locked after 5 failed login attempts."},
    ]
    from agents.schemas import SynthesisRequest
    req = SynthesisRequest(query="Password policy", retrieved_chunks=mock_chunks)
    draft = agent.handle(req)
    print(draft)