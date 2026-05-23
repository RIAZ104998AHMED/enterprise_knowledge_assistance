# rag/ingestion.py
import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize
from config import settings

# Paths
VECTOR_STORE_PATH = "rag/vector_store.faiss"
DOC_CHUNKS_PATH = "rag/doc_chunks.pkl"
CORPUS_DIR = "corpus/documents"  # folder with markdown files
# Alternatively, if using single combined file:
COMBINED_CORPUS_PATH = "corpus/corpus_combined.md"

# Load embedding model
model = SentenceTransformer(settings.EMBEDDING_MODEL)

def chunk_text(text, chunk_size=settings.CHUNK_SIZE, overlap=settings.CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_len = 0
    for s in sentences:
        current_chunk.append(s)
        current_len += len(s.split())
        if current_len >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = current_chunk[-overlap:]
            current_len = sum(len(x.split()) for x in current_chunk)
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def ingest_documents_from_folder(folder_path="corpus/documents"):
    chunks = []
    for fname in sorted(os.listdir(folder_path)):
        path = os.path.join(folder_path, fname)
        if fname.endswith(".md"):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            chunks.append({"id": fname, "text": text})
    return chunks

def ingest_documents_from_file(file_path=COMBINED_CORPUS_PATH):
    """Read a single combined Markdown corpus and chunk by double newline."""
    all_chunks = []
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # Split by double newlines
    sections = [s.strip() for s in text.split("\n\n") if s.strip()]
    for i, sec in enumerate(sections):
        chunks = chunk_text(sec)
        for j, chunk in enumerate(chunks):
            all_chunks.append({"id": f"section_{i}_{j}", "text": chunk})
    return all_chunks

def build_vector_store(chunks):
    """Embed all chunks and build FAISS index."""
    print(f"Building vector store for {len(chunks)} chunks...")
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, VECTOR_STORE_PATH)
    with open(DOC_CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Vector store saved to {VECTOR_STORE_PATH} and chunks to {DOC_CHUNKS_PATH}.")

if __name__ == "__main__":
    os.makedirs("rag", exist_ok=True)
    # Option 1: Ingest folder
    chunks = ingest_documents_from_folder()
    # Option 2: Ingest single combined file (uncomment if using combined)
    # chunks = ingest_documents_from_file()
    build_vector_store(chunks)