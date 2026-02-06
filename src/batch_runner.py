import csv
from typing import List, Dict

from session_controller import SessionController
from query_interpreter import QueryInterpreter
from reasoning_router import ReasoningRouter
from response_generator import ResponseGenerator
from reasoning_engine import CausalReasoningEngine
from causal_aggregator import aggregate_causal_explanations
from final_explainer import FinalCausalExplainer
class EscalationCausalSystem:
    def __init__(self):
        self.engine = CausalReasoningEngine()
        self.explainer = FinalCausalExplainer()

    def run(self, query: str) -> Dict:
        reasoning_output = self.engine.answer_query(
            query=query,
            outcome="ESCALATION",
            top_k=5
        )

        reasoning_output["global_causal_explanation"] = (
            aggregate_causal_explanations(
                reasoning_output.get("supporting_calls", [])
            )
        )

        return self.explainer.generate_explanation(reasoning_output)

QUERIES: List[Dict] = [
    {"id": "Q1", "query": "Why did the customer ask for a supervisor multiple times?", "category": "Escalation Reason"},
    {"id": "Q2", "query": "Was it because the agent refused a refund?", "category": "Policy Constraint"},
    {"id": "Q3", "query": "Did repeated transfers cause the escalation?", "category": "Operational Failure"},
    {"id": "Q4", "query": "Was legal action mentioned by the customer?", "category": "Threat Detection"},
    {"id": "Q5", "query": "Did unresolved technical issues lead to escalation?", "category": "Technical Issue"},
    {"id": "Q6", "query": "Was the agent unable to resolve the issue?", "category": "Agent Performance"},
    {"id": "Q7", "query": "Did long wait times contribute to escalation?", "category": "Service Delay"},
    {"id": "Q8", "query": "Was the escalation emotionally driven?", "category": "Sentiment"},
    {"id": "Q9", "query": "Did the customer threaten to cancel the service?", "category": "Churn Risk"},
    {"id": "Q10", "query": "Did policy restrictions prevent resolution?", "category": "Policy Constraint"},
]
def run_batch(output_csv: str = "evaluation_results.csv"):

    session_controller = SessionController()
    query_interpreter = QueryInterpreter()
    reasoning_router = ReasoningRouter()
    response_generator = ResponseGenerator()
    causal_system = EscalationCausalSystem()

    rows = []

    for item in QUERIES:
        user_query = item["query"]
        request = session_controller.prepare_request(user_query)
        interpreted = query_interpreter.interpret(
            request["current_query"],
            request["prior_context"]
        )
        plan = reasoning_router.route(
            interpreted,
            request["prior_context"]
        )
        final_query = (
            plan.get("query")
            if isinstance(plan, dict) and "query" in plan
            else interpreted.get("query", user_query)
            if isinstance(interpreted, dict)
            else user_query
        )
        result = causal_system.run(final_query)
        output_text = response_generator.generate(
            reasoning_output=result,
            session_context=request["prior_context"],
            user_query=user_query
        )
        session_controller.store_result(
            user_query=user_query,
            system_result=result
        )
        rows.append([
            item["id"],
            user_query,
            item["category"],
            output_text.replace("\n", " "),
            "IDRecall, Faithfulness, Relevancy auto-computed"
        ])
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Query-Id",
            "Query",
            "Query-Category",
            "System-Output",
            "Remarks"
        ])
        writer.writerows(rows)

    print(f"\n✅ Batch evaluation completed successfully → {output_csv}\n")
if __name__ == "__main__":
    run_batch()
