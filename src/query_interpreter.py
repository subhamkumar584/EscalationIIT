from typing import Dict, Optional


class QueryInterpreter:
    FOLLOW_UP_KEYWORDS = {
        "again",
        "same",
        "earlier",
        "previous",
        "that",
        "those",
        "this",
        "above",
        "already",
        "before"
    }

    EVIDENCE_KEYWORDS = {
        "evidence",
        "proof",
        "example",
        "show",
        "where",
        "which call",
        "which conversation"
    }

    COMPARISON_KEYWORDS = {
        "compare",
        "difference",
        "different",
        "similar",
        "versus",
        "vs"
    }

    SUMMARY_KEYWORDS = {
        "summarize",
        "summary",
        "brief",
        "short",
        "overall"
    }

    def interpret(
        self,
        query: str,
        previous_context: Optional[Dict] = None
    ) -> Dict:
        normalized_query = query.lower()

        query_type = self._detect_query_type(
            normalized_query,
            previous_context
        )

        return {
            "original_query": query,
            "query_type": query_type,
            "is_follow_up": query_type != "NEW_CAUSAL_QUERY",
            "requires_context": previous_context is not None
            and query_type != "NEW_CAUSAL_QUERY",
            "focus_outcome": self._infer_outcome(normalized_query),
        }
    def _detect_query_type(
        self,
        query: str,
        previous_context: Optional[Dict]
    ) -> str:

        if self._contains_any(query, self.SUMMARY_KEYWORDS):
            return "SUMMARY_REQUEST"

        if self._contains_any(query, self.EVIDENCE_KEYWORDS):
            return "EVIDENCE_REQUEST"

        if self._contains_any(query, self.COMPARISON_KEYWORDS):
            return "COMPARATIVE_QUERY"

        if previous_context and self._contains_any(
            query,
            self.FOLLOW_UP_KEYWORDS
        ):
            return "FOLLOW_UP_QUERY"

        return "NEW_CAUSAL_QUERY"

    def _infer_outcome(self, query: str) -> Optional[str]:
        if "escalat" in query:
            return "ESCALATION"
        if "refund" in query:
            return "REFUND"
        if "complaint" in query:
            return "COMPLAINT"

        return None

    def _contains_any(self, query: str, keywords: set) -> bool:
        return any(keyword in query for keyword in keywords)
