
# main.py
from agents.orchestrator import Orchestrator
from safety.input_guards import check_input
from config import settings

def main():
    orchestrator = Orchestrator()
    print("=== Enterprise Knowledge Assistant ===")
    print("Type your query or 'exit' to quit.\n")

    while True:
        query = input("Enter your question: ").strip()
        if query.lower() == "exit":
            print("Exiting. Goodbye!")
            break

        # Input guardrails
        incidents = check_input(query)
        if incidents:
            print(f"Input blocked due to guardrail triggers: {incidents}\n")
            continue

        # Orchestrator workflow
        draft, verdict = orchestrator.handle_query(query, role=settings.DEFAULT_USER_ROLE)

        # Display results
        print("\n--- Answer ---")
        print(draft.get("answer", "No answer generated."))
        print("\n--- Citations ---")
        print(draft.get("citations", []))
        print("\n--- Safety ---")
        print(f"Approved: {verdict.approved} | Notes: {verdict.notes}\n")
        print("="*50 + "\n")

if __name__ == "__main__":
    main()