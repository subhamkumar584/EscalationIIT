from typing import Dict, List
from collections import defaultdict


class OutcomeValidator:
    def __init__(self, min_support: int = 2):
        self.min_support = min_support

    def validate(
        self,
        query: str,
        outcome: str,
        step6_output: Dict
    ) -> Dict:
        supporting_calls = step6_output.get("supporting_calls", [])

        if len(supporting_calls) < self.min_support:
            return self._no_outcome_response(query, outcome)

        escalation_types = defaultdict(int)
        evidence_map = defaultdict(list)

        for call in supporting_calls:
            for factor in call["causal_explanation"]["causal_factors"]:
                escalation_types[factor["factor"]] += 1
                evidence_map[factor["factor"]].extend(
                    factor["evidence_turns"]
                )

        identified_types = [
            {
                "escalation_type": factor,
                "supporting_calls": count,
                "sample_evidence": evidence_map[factor][:2]
            }
            for factor, count in escalation_types.items()
            if count >= self.min_support
        ]

        if not identified_types:
            return self._no_outcome_response(query, outcome)

        return {
            "query": query,
            "outcome_confirmed": True,
            "outcome": outcome,
            "escalation_types": identified_types,
            "justification": (
                f"The query implies {outcome} based on recurring "
                f"dialogue patterns observed across multiple conversations."
            )
        }

    def _no_outcome_response(self, query: str, outcome: str) -> Dict:
        return {
            "query": query,
            "outcome_confirmed": False,
            "outcome": outcome,
            "justification": (
                "Insufficient conversational evidence to confirm "
                f"that the query results in {outcome}."
            )
        }
