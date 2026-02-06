from collections import defaultdict
from typing import List, Dict

def aggregate_causal_explanations(
    supporting_calls: List[Dict],
    top_k: int = 3
) -> Dict:
    factor_stats = defaultdict(lambda: {
        "supporting_calls": 0,
        "total_score": 0.0
    })

    for call in supporting_calls:
        causal_exp = call["causal_explanation"]

        for factor in causal_exp["causal_factors"]:
            name = factor["factor"]
            factor_stats[name]["supporting_calls"] += 1
            factor_stats[name]["total_score"] += factor["evidence_score"]

    aggregated = []
    for factor, stats in factor_stats.items():
        aggregated.append({
            "factor": factor,
            "supporting_calls": stats["supporting_calls"],
            "avg_evidence_score": round(
                stats["total_score"] / stats["supporting_calls"], 3
            ),
            "causal_strength": round(
                stats["supporting_calls"] * stats["total_score"], 3
            )
        })

    aggregated.sort(
        key=lambda x: (x["supporting_calls"], x["causal_strength"]),
        reverse=True
    )

    return {
        "num_global_factors": len(aggregated[:top_k]),
        "global_causal_factors": aggregated[:top_k]
    }
