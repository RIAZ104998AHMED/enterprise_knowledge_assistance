# Enterprise Knowledge Assistant

A secure Multi-Agent Retrieval-Augmented Generation (RAG) system designed to answer user queries from a knowledge base while maintaining safety, grounding, and citation transparency.

## Overview

This project implements an enterprise-grade knowledge assistant using a modular agent architecture. The system retrieves relevant information from a document corpus, generates grounded responses with citations, and applies multiple safety layers before returning the final answer.

The assistant combines:

- Hybrid Retrieval (FAISS + BM25)
- Cross-Encoder Re-ranking
- Multi-Agent Orchestration
- Input and Output Guardrails
- Citation-Based Responses
- PII Detection and Redaction
- Retrieval Evaluation Framework
- Red-Team Security Testing

---

## Architecture

```text
User Query
    │
    ▼
Input Guardrails
    │
    ▼
Orchestrator
    │
 ┌──┼─────────────┐
 ▼  ▼             ▼
Retriever    Synthesizer    Reviewer
Agent         Agent          Agent
 │              │             │
 ▼              ▼             ▼
Hybrid      Answer      Grounding Check
Retrieval   Generation  + PII Redaction
 │
 ▼
FAISS + BM25
 │
 ▼
Cross Encoder Re-ranking
 │
 ▼
Final Answer + Citations
```

---

## Features

### Retrieval
- Dense retrieval using Sentence Transformers
- Sparse retrieval using BM25
- Hybrid retrieval fusion
- FAISS vector database
- Cross-Encoder re-ranking

### Safety
- Prompt injection detection
- Jailbreak detection
- PII detection
- PII redaction
- Grounding verification
- Role-based access control (RBAC)

### Evaluation
- Recall@K
- Mean Reciprocal Rank (MRR)
- Adversarial Red-Team Testing

### Multi-Agent Workflow
- Retriever Agent
- Synthesizer Agent
- Reviewer Agent
- Central Orchestrator

---

## Project Structure

```text
Enterprise-Knowledge-Assistant/
│
├── agents/
│   ├── orchestrator.py
│   ├── retriever_agent.py
│   ├── synthesizer_agent.py
│   ├── reviewer_agent.py
│   └── schemas.py
│
├── rag/
│   ├── ingestion.py
│   ├── retrieve.py
│   └── reranking.py
│
├── safety/
│   ├── input_guards.py
│   ├── output_guards.py
│   └── incident_log.py
│
├── eval/
│   ├── run_eval.py
│   ├── labeled_questions.json
│   └── red_team_set.json
│
├── corpus/
│   └── documents/
│
├── logs/
│
├── config/
│   └── settings.py
│
├── main.py
├── requirements.txt
└── .env.example
```

---

## Workflow

### Step 1: Input Validation

The user's query is checked for:

- Prompt Injection
- Jailbreak Attempts
- Personally Identifiable Information (PII)

If a violation is detected, the query is blocked and logged.

---

### Step 2: Retrieval

The Retriever Agent:

1. Performs Dense Retrieval using Sentence Transformers and FAISS.
2. Performs Sparse Retrieval using BM25.
3. Combines results using Hybrid Retrieval.
4. Re-ranks candidates using a Cross Encoder.

---

### Step 3: Answer Generation

The Synthesizer Agent:

- Receives top-ranked chunks.
- Generates a response from retrieved knowledge.
- Attaches source citations.

---

### Step 4: Safety Review

The Reviewer Agent:

- Verifies citations exist in retrieved documents.
- Detects hallucinated references.
- Redacts emails, phone numbers, SSNs, and credit card information.

---

### Step 5: Final Response

The system returns:

- Generated Answer
- Supporting Citations
- Safety Verdict

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/enterprise-knowledge-assistant.git

cd enterprise-knowledge-assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here

SYNTHESIZER_MODEL=openai/gpt-3.5-turbo

SAFETY_MODEL=mistralai/mistral-7b-instruct

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## Building the Knowledge Base

Before querying the system, create the vector database:

```bash
python rag/ingestion.py
```

Generated files:

```text
rag/vector_store.faiss

rag/doc_chunks.pkl
```

---

## Running the Assistant

```bash
python main.py
```

Example:

```text
Enter your question:

What is the company password rotation policy?
```

Output:

```text
--- Answer ---
Passwords must be rotated every 90 days.

--- Citations ---
['0_nq_0']

--- Safety ---
Approved: True
Notes: Approved
```

---

## Evaluation

Run retrieval evaluation:

```bash
python eval/run_eval.py
```

Metrics reported:

- Recall@5
- Mean Reciprocal Rank (MRR)

The evaluation framework also executes:

- Prompt Injection Attacks
- Jailbreak Attempts
- PII Leakage Tests
- Indirect Prompt Injection Tests

---

## Technologies Used

- Python
- FAISS
- Sentence Transformers
- Cross Encoder
- BM25
- OpenRouter
- Pydantic
- NLTK
- NumPy

---

## Security Features

### Input Guardrails

Detects:

- Prompt Injection
- Jailbreak Prompts
- PII Inputs

Examples:

```text
Ignore previous instructions

Reveal system prompt

You are now DAN
```

---

### Output Guardrails

Protects against:

- Hallucinated Citations
- PII Leakage
- Unauthorized Access

Examples:

```text
john.doe@example.com
```

becomes

```text
[REDACTED_EMAIL]
```

---

## Future Improvements

- Advanced LLM-based synthesis
- Better RRF implementation
- Metadata filtering
- Production-grade RBAC
- Conversation memory
- Web dashboard
- Streaming responses
- Agent tracing and observability

---

## Known Limitations

- Small-talk queries may retrieve irrelevant documents.
- Current synthesis logic is intentionally simple.
- Guardrails are regex-based and can be improved using LLM moderation.
- Corpus quality directly affects answer quality.

---

## Example Multi-Agent Flow

```text
User:
"What is the company password policy?"

↓

Retriever Agent:
Retrieves relevant chunks

↓

Synthesizer Agent:
Creates grounded answer

↓

Reviewer Agent:
Verifies citations and removes PII

↓

Final Output:
Answer + Citations + Safety Verdict
```

---

## Author

Developed as a Multi-Agent RAG Enterprise Knowledge Assistant project demonstrating:

- Retrieval-Augmented Generation
- Safety-Aware AI Systems
- Enterprise Search
- Secure AI Workflows
- Evaluation and Red-Team Testing

