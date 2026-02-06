from typing import Dict, Any


class ReasoningRouter:
    def route(
        self,
        intent_payload: Dict[str, Any],
        session_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        intent_type = intent_payload.get("intent_type")
        if intent_type == "NEW_CAUSAL_QUERY":
            return {
                "action": "RUN_FULL_CAUSAL_ANALYSIS",
                "use_previous_context": False
            }
        if intent_type == "FOLLOW_UP_WHY":
            return {
                "action": "REFINE_EXISTING_EXPLANATION",
                "use_previous_context": True,
                "focus_factors": intent_payload.get("focus_factors", [])
            }

        if intent_type == "ASK_EVIDENCE":
            return {
                "action": "RETURN_SUPPORTING_EVIDENCE",
                "use_previous_context": True
            }
        if intent_type == "ASK_SUMMARY":
            return {
                "action": "SUMMARIZE_PREVIOUS_RESULT",
                "use_previous_context": True
            }
        return {
            "action": "REQUEST_CLARIFICATION",
            "use_previous_context": False,
            "message": "Could you clarify what you want to explore further?"
        }
