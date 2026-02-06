from typing import Dict, List


class FinalCausalExplainer:
    def generate_explanation(self, reasoning_output: Dict) -> Dict:
        if reasoning_output.get("num_supporting_calls", 0) == 0:
            return {
                "query": reasoning_output.get("query"),
                "outcome": "NOT_ESCALATION",
                "escalation_confirmed": False,
                "explanation": "No sufficient conversational evidence was found to support escalation.",
                "confidence": "LOW"
            }
        global_explanation = reasoning_output.get("global_causal_explanation", {})
        global_factors = global_explanation.get("global_causal_factors", [])

        why_it_happened = []

        for factor in global_factors:
            why_it_happened.append({
                "cause": factor["factor"],
                "causal_strength": round(factor["causal_strength"], 2),
                "supporting_calls": factor["supporting_calls"],
                "avg_evidence_score": round(factor["avg_evidence_score"], 2),
                "explanation": (
                    f"The escalation is driven by '{factor['factor']}', "
                    f"which consistently appears across "
                    f"{factor['supporting_calls']} conversations."
                )
            })
        sample_evidence = []

        for call in reasoning_output.get("supporting_calls", [])[:2]:
            for factor in call["causal_explanation"].get("causal_factors", []):
                turns = factor.get("evidence_turns", [])
                if not turns:
                    continue

                turn = turns[0]
                sample_evidence.append({
                    "transcript_id": call["transcript_id"],
                    "factor": factor["factor"],
                    "turn_id": turn["turn_id"],
                    "speaker": turn["speaker"],
                    "text": turn["text"]
                })
        return {
            "query": reasoning_output.get("query"),
            "outcome": reasoning_output.get("outcome"),
            "escalation_confirmed": True,
            "num_supporting_calls": reasoning_output.get("num_supporting_calls"),
            "why_it_happened": why_it_happened,
            "evidence_snippets": sample_evidence,
            "final_summary": self._build_summary(why_it_happened),
            "confidence": "HIGH"
        }

    def _build_summary(self, causes: List[Dict]) -> str:
        if not causes:
            return "No dominant causal factors were identified."

        cause_names = [c["cause"] for c in causes]

        return (
            "The escalation occurred primarily due to "
            + ", ".join(cause_names)
            + ", as evidenced by repeated and unresolved customer-agent interactions."
        )
