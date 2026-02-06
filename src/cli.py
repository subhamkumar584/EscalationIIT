from reasoning_engine import CausalReasoningEngine
from causal_aggregator import aggregate_causal_explanations
from final_explainer import FinalCausalExplainer

from session_controller import SessionController
from query_interpreter import QueryInterpreter
from reasoning_router import ReasoningRouter
from response_generator import ResponseGenerator


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
        return self.explainer.generate_explanation(reasoning_output)


def main():
    print("\n=== Escalation Causal Explanation System (Task 2 Enabled) ===\n")
    print("Ask WHY-type questions. Type 'exit' to quit.\n")

    session_controller = SessionController()
    query_interpreter = QueryInterpreter()
    reasoning_router = ReasoningRouter()
    response_generator = ResponseGenerator()
    causal_system = EscalationCausalSystem()

    while True:
        user_query = input("> ").strip()

        if not user_query:
            print("❌ Query cannot be empty.\n")
            continue

        if user_query.lower() in {"exit", "quit"}:
            print("\n👋 Ending session. Goodbye!")
            break
        request = session_controller.prepare_request(user_query)
        interpreted = query_interpreter.interpret(
            request["current_query"],
            request["prior_context"]
        )
        reasoning_plan = reasoning_router.route(
            interpreted,
            request["prior_context"]
        )
        final_query = (
            reasoning_plan.get("query")
            or reasoning_plan.get("resolved_query")
            or interpreted.get("query")
            or request["current_query"]
        )
        result = causal_system.run(
            query=final_query,
            outcome=reasoning_plan.get("outcome", "ESCALATION"),
            top_k=reasoning_plan.get("top_k", 5)
        )
        session_controller.store_result(
            user_query=user_query,
            system_result=result
        )
        response_generator.display(result)
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
