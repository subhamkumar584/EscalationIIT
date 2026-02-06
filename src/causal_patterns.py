import re
from typing import List, Dict
from collections import defaultdict

CAUSAL_PATTERNS = {
    "Repeated unresolved issue": [
        r"\balready explained\b",
        r"\bmultiple times\b",
        r"\bseveral times\b",
        r"\bagain and again\b",
        r"\bfor weeks\b",
        r"\bfor days\b"
    ],
    "Issue not resolved": [
        r"\bstill not working\b",
        r"\bnot resolved\b",
        r"\bissue persists\b",
        r"\bnothing has changed\b"
    ],
    "Request for supervisor": [
        r"\bspeak to (a )?supervisor\b",
        r"\btalk to (a )?manager\b",
        r"\bescalate this\b"
    ],
    "Threat of legal action": [
        r"\blawyer\b",
        r"\blegal action\b",
        r"\bsue\b"
    ],
    "Customer frustration": [
        r"\bfrustrated\b",
        r"\bupset\b",
        r"\bangry\b",
        r"\btired of\b"
    ]
}

def extract_causal_explanation(
    conversation: List[Dict],
    outcome: str
) -> Dict:
    factor_to_evidence = defaultdict(list)
    customer_turns = [
        i for i, t in enumerate(conversation)
        if t["speaker"].lower() == "customer"
    ]
    total_customer_turns = max(len(customer_turns), 1)

    for turn_id, turn in enumerate(conversation):
        text = turn["text"].lower()

        for factor, patterns in CAUSAL_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    factor_to_evidence[factor].append({
                        "turn_id": turn_id,
                        "speaker": turn["speaker"],
                        "text": turn["text"]
                    })
                    break

    causal_factors = []

    for factor, evidence_turns in factor_to_evidence.items():
        unique_turns = {e["turn_id"] for e in evidence_turns}

        evidence_score = round(
            len(evidence_turns) / len(conversation),2
        )

        causal_factors.append({
            "factor": factor,
            "evidence_score": evidence_score,
            "evidence_turns": evidence_turns
        })

    return {
        "outcome": outcome,
        "num_factors": len(causal_factors),
        "causal_factors": causal_factors
    }
