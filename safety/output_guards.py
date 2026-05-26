# safety/output_guards.py
import re

def grounding_check(response, retrieved_chunks):
    """
    Ensure every citation in the response exists in the retrieved chunks.
    Args:
        response (dict): Contains 'answer' and optional 'citations' list.
        retrieved_chunks (list): List of dicts with 'id' keys.
    Returns:
        List of missing citation IDs.
    """
    missing = []
    citations = response.get("citations", [])
    chunk_ids = [c["id"] for c in retrieved_chunks]
    for cid in citations:
        if cid not in chunk_ids:
            missing.append(cid)
    return missing

def redact_pii(text):
    """
    Redact sensitive information in the response.
    Supports emails, phone numbers, SSNs.
    """
    text = re.sub(r"\S+@\S+\.\S+", "[REDACTED_EMAIL]", text)
    text = re.sub(r"\b\d{10}\b", "[REDACTED_PHONE]", text)
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", text)
    text = re.sub(r"\b\d{12,16}\b", "[REDACTED_CREDITCARD]", text)
    return text

def rbac_filter(retrieved_chunks, user_role="intern"):
    """
    Filter chunks based on a 'min_role' metadata field.
    Only chunks with min_role <= user_role are returned.
    Example role hierarchy: intern < employee < manager < admin
    """
    role_hierarchy = {"intern": 0, "employee": 1, "manager": 2, "admin": 3}
    user_level = role_hierarchy.get(user_role, 0)
    filtered = []
    for c in retrieved_chunks:
        min_role = c.get("min_role", "intern")
        if role_hierarchy.get(min_role, 0) <= user_level:
            filtered.append(c)
    return filtered

if __name__ == "__main__":
    # Quick test
    response = {
        "answer": "Contact john.doe@example.com or call 1234567890.",
        "citations": ["chunk_1", "chunk_2"]
    }
    retrieved_chunks = [{"id": "chunk_1"}, {"id": "chunk_2"}]
    missing = grounding_check(response, retrieved_chunks)
    print("Missing citations:", missing)

    redacted = redact_pii(response["answer"])
    print("Redacted answer:", redacted)

    # RBAC test
    chunks = [{"id":"chunk_a","min_role":"manager"}, {"id":"chunk_b","min_role":"intern"}]
    filtered = rbac_filter(chunks, user_role="intern")
    print("Filtered chunks:", filtered)