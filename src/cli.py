from reasoning_engine import CausalReasoningEngine
from causal_aggregator import aggregate_causal_explanations
from final_explainer import FinalCausalExplainer


class EscalationCausalSystem:
    def __init__(self):
        self.reasoning_engine = CausalReasoningEngine()
        self.explainer = FinalCausalExplainer()

    def run(self, query: str, outcome: str = "ESCALATION", top_k: int = 5):
        reasoning_output = self.reasoning_engine.answer_query(
            query=query,
            outcome=outcome,
            top_k=top_k
        )
        global_causal_explanation = aggregate_causal_explanations(
            supporting_calls=reasoning_output["supporting_calls"]
        )
        reasoning_output["global_causal_explanation"] = global_causal_explanation
        final_output = self.explainer.generate_explanation(reasoning_output)

        return final_output
if __name__ == "__main__":
    print("\n=== Escalation Causal Explanation System ===\n")

    user_query = input("Ask your question (WHY-type):\n> ").strip()

    if not user_query:
        print("❌ Query cannot be empty.")
        exit(1)

    system = EscalationCausalSystem()
    result = system.run(user_query)
    print("\n=== Explanation ===\n")

    if not result.get("escalation_confirmed", False):
        print("❌ No escalation was identified.")
        print(result.get("explanation", "No sufficient evidence found."))
        exit(0)

    print(f"📌 Outcome: {result['outcome']}")
    print(f"📊 Confidence: {result['confidence']}\n")

    print("🔍 Why did this escalation happen?")
    for idx, cause in enumerate(result["why_it_happened"], 1):
        print(
            f"{idx}. {cause['cause']} "
            f"(seen in {cause['supporting_calls']} conversations)"
        )

    print("\n🧾 Supporting Evidence:")
    for ev in result["evidence_snippets"]:
        print(
            f"- [{ev['transcript_id']} | Turn {ev['turn_id']}] "
            f"{ev['speaker']}: \"{ev['text']}\""
        )

    print("\n📝 Final Summary:")
    print(result["final_summary"])
