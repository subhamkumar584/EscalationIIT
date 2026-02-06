

from typing import Dict
from data_loader import ConversationDataset
from retriever import HybridRetriever
from causal_patterns import extract_causal_explanation
from causal_aggregator import aggregate_causal_explanations


class CausalReasoningEngine:
    def __init__(self):
        self.dataset = ConversationDataset()
        self.retriever = HybridRetriever(self.dataset)

    def answer_query(
        self,
        query: str,
        outcome: str,
        top_k: int = 5
    ) -> Dict:

        retrieved = self.retriever.search(query, top_k=top_k)
        supporting_calls = []

        for item in retrieved:
            transcript_id = item["transcript_id"]
            conv = self.dataset.get_conversation(transcript_id)

            causal_explanation = extract_causal_explanation(
                conversation=conv["conversation"],
                outcome=outcome
            )
            if causal_explanation["num_factors"] == 0:
                continue

            supporting_calls.append({
                "transcript_id": transcript_id,
                "domain": conv["domain"],
                "intent": conv["intent"],
                "retrieval_score": round(item["score"], 3),
                "causal_explanation": causal_explanation
            })

        global_causal_explanation = aggregate_causal_explanations(
            supporting_calls=supporting_calls,
            top_k=3
        )

        return {
            "query": query,
            "outcome": outcome,
            "num_supporting_calls": len(supporting_calls),
            "supporting_calls": supporting_calls,
            "global_causal_explanation": global_causal_explanation
        }

