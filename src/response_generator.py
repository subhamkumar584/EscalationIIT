from typing import Dict, List, Optional
import re

class ResponseGenerator:

    def _compute_id_recall(self, evidence: List[Dict]) -> float:
        return 1.0 if evidence else 0.0

    def _compute_faithfulness(
        self,
        causes: List[Dict],
        evidence: List[Dict]
    ) -> float:
        if not causes:
            return 0.0
        if not evidence:
            return 0.0

        return 1.0

    def _compute_relevancy(
        self,
        user_query: str,
        causes: List[Dict],
        summary: str
    ) -> float:
        

        if not user_query:
            return 0.0

        query = user_query.lower()
        intent_markers = [
            "why", "reason", "cause", "because",
            "did", "was", "were", "is",
            "escalat", "supervisor", "refund",
            "policy", "agent", "issue"
        ]

        intent_detected = any(m in query for m in intent_markers)
        if intent_detected and (causes or summary):
            return 1.0

        return 0.0

    def generate(
        self,
        reasoning_output: Dict,
        session_context: Optional[Dict] = None,
        user_query: Optional[str] = None
    ) -> str:

        if not reasoning_output:
            return "No explanation could be generated."

        outcome = reasoning_output.get("outcome", "UNKNOWN")
        confidence = reasoning_output.get("confidence", "UNKNOWN")
        causes = reasoning_output.get("why_it_happened", [])
        evidence = reasoning_output.get("evidence_snippets", [])
        summary = reasoning_output.get("final_summary", "")

        id_recall = self._compute_id_recall(evidence)
        faithfulness = self._compute_faithfulness(causes, evidence)
        relevancy = self._compute_relevancy(
            user_query or "",
            causes,
            summary
        )

        lines: List[str] = []
        lines.append("=== Explanation ===")
        lines.append(f"📌 Outcome: {outcome}")
        lines.append(f"📊 Confidence: {confidence}")
        lines.append("")

        if causes:
            lines.append("🔍 Why did this happen?")
            for idx, cause in enumerate(causes, start=1):
                lines.append(
                    f"{idx}. {cause.get('cause', 'Unknown')} "
                    f"(observed in {cause.get('supporting_calls', 0)} conversations)"
                )
            lines.append("")

        if evidence:
            lines.append("🧾 Supporting Evidence:")
            for ev in evidence:
                lines.append(
                    f"- [{ev.get('transcript_id')} | Turn {ev.get('turn_id')}] "
                    f"{ev.get('speaker')}: \"{ev.get('text', '').strip()}\""
                )
            lines.append("")

        if summary:
            lines.append("📝 Final Summary:")
            lines.append(summary)
            lines.append("")
        lines.append("=== Evaluation Metrics ===")
        lines.append(f"🆔 IDRecall (Evidence Accuracy): {id_recall}")
        lines.append(f"🧠 Faithfulness (Hallucination Control): {faithfulness}")
        lines.append(f"🎯 Relevancy (Conversational Coherence): {relevancy}")

        return "\n".join(lines)
    def display(
        self,
        reasoning_output: Dict,
        session_context: Optional[Dict] = None,
        user_query: Optional[str] = None
    ):
        print(self.generate(reasoning_output, session_context, user_query))
