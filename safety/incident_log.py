# safety/incident_log.py
import os
import json
from datetime import datetime

# Log file path
INCIDENT_LOG = "logs/incidents.jsonl"
os.makedirs("logs", exist_ok=True)

def log_incident(rule_name, input_text, user_role=None, extra_info=None):
    """
    Log a guardrail incident in structured JSONL format.

    Args:
        rule_name (str): Name of the guardrail that triggered
        input_text (str): User input or content that triggered the rule
        user_role (str, optional): Role of the user (intern, employee, manager)
        extra_info (dict, optional): Any additional information
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "rule": rule_name,
        "input": input_text,
        "user_role": user_role if user_role else "unknown",
        "extra_info": extra_info if extra_info else {}
    }

    with open(INCIDENT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def read_incidents():
    """
    Read all incidents from the JSONL log.
    Returns:
        List of dict entries
    """
    incidents = []
    if os.path.exists(INCIDENT_LOG):
        with open(INCIDENT_LOG, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    incidents.append(json.loads(line))
    return incidents

if __name__ == "__main__":
    # Test logging
    log_incident("prompt_injection", "Ignore previous instructions", user_role="intern")
    log_incident("pii_detected", "My email is john.doe@example.com")
    all_incidents = read_incidents()
    print("Logged incidents:")
    for i, inc in enumerate(all_incidents, 1):
        print(f"{i}. {inc}")