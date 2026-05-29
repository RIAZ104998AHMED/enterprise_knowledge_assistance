# agents/schemas.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class RetrievalRequest(BaseModel):
    query: str
    top_k: int = 10
    role: str = "intern"  # user role: intern, employee, manager, admin


class RetrievalResult(BaseModel):
    chunks: List[Dict[str, Any]]  # Each chunk: {"id": str, "text": str, "score": float, ...}


class SynthesisRequest(BaseModel):
    query: str
    retrieved_chunks: List[Dict[str, Any]]
    role: str = "intern"


class SynthesisResult(BaseModel):
    draft: Dict[str, Any]  # {"answer": str, "citations": List[str]}
    citations: List[str]


class SafetyVerdict(BaseModel):
    approved: bool
    notes: str
    redacted_draft: Optional[Dict[str, Any]] = None


class FinalAnswer(BaseModel):
    answer: str
    citations: List[str]


# Pydantic v2 fix: rebuild models if needed
RetrievalResult.model_rebuild()
SynthesisRequest.model_rebuild()
SynthesisResult.model_rebuild()
SafetyVerdict.model_rebuild()
FinalAnswer.model_rebuild()
RetrievalRequest.model_rebuild()