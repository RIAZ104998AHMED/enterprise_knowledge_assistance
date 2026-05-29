# eval/run_eval.py
import json
from agents.orchestrator import Orchestrator
from safety.input_guards import check_input

# Load evaluation sets
with open("eval/labeled_questions.json", "r", encoding="utf-8") as f:
    labeled_qs = json.load(f)

with open("eval/red_team_set.json", "r", encoding="utf-8") as f:
    red_team_prompts = json.load(f)

def recall_at_k(retrieved_ids, ground_truth, k=5):
    """
    Recall@k: fraction of ground truth IDs found in top-k retrieved.
    """
    retrieved_topk = set(retrieved_ids[:k])
    return len(set(ground_truth) & retrieved_topk) / len(ground_truth)

def mrr(retrieved_ids, ground_truth):
    """
    Mean Reciprocal Rank: 1 / rank of first relevant retrieved chunk
    """
    for i, rid in enumerate(retrieved_ids, 1):
        if rid in ground_truth:
            return 1.0 / i
    return 0.0

def run_retrieval_eval():
    """
    Evaluate all labeled questions and print average Recall@5 and MRR.
    """
    orchestrator = Orchestrator()
    recalls, mrrs = [], []

    print("Running retrieval evaluation on labeled questions...")
    for q in labeled_qs:
        draft, _ = orchestrator.handle_query(q["question"])
        retrieved_ids = draft.get("citations", [])
        recalls.append(recall_at_k(retrieved_ids, q["ground_truth"]))
        mrrs.append(mrr(retrieved_ids, q["ground_truth"]))

    avg_recall = sum(recalls) / len(recalls)
    avg_mrr = sum(mrrs) / len(mrrs)
    print(f"\nAverage Recall@5: {avg_recall:.2f}")
    print(f"Average MRR: {avg_mrr:.2f}")

def run_red_team_eval():
    """
    Run adversarial prompts to check input guardrails.
    """
    orchestrator = Orchestrator()
    print("\nRunning red-team evaluation...")
    for attack in red_team_prompts:
        incidents = check_input(attack["prompt"])
        result = "PASSED" if incidents else "BYPASSED"
        print(f"Attack type: {attack['type']} | Guardrail triggered: {incidents} | Result: {result}")

if __name__ == "__main__":
    run_retrieval_eval()
    run_red_team_eval()