# config/settings.py
# ----------------------
# RAG / Retrieval Settings
# ----------------------
CHUNK_SIZE = 400         # Number of tokens per chunk
CHUNK_OVERLAP = 80       # Overlap between chunks
TOP_K = 10               # Number of top candidates to retrieve
RERANK_TOP_N = 5         # Number of candidates to return after reranking

# ----------------------
# Embedding & LLM Models
# ----------------------
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
SYNTHESIZER_MODEL = "openai/gpt-3.5-turbo"
OPENROUTER_API_KEY = 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
SAFETY_MODEL = "mistralai/mistral-7b-instruct"

# ----------------------
# Logging
# ----------------------
INCIDENT_LOG_PATH = "logs/incidents.jsonl"
TRACE_LOG_PATH = "logs/traces.jsonl"

# ----------------------
# Other Config
# ----------------------
MAX_ROUNDS = 3           # Max retry loop for safety feedback
DEFAULT_USER_ROLE = "intern"
