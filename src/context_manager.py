from typing import Dict, Optional, List
from context_store import ContextStore


class ContextManager:
    def __init__(self, store: ContextStore):
        self.store = store

    def start_session(self, session_id: str):
        self.store.create_session(session_id)

    def end_session(self, session_id: str):
        self.store.reset_session(session_id)

    def update_context(
        self,
        session_id: str,
        user_query: str,
        system_response: Dict
    ):

        turn_context = {
            "query": user_query,
            "outcome": system_response.get("outcome"),
            "causal_factors": [
                factor["cause"]
                for factor in system_response.get("why_it_happened", [])
            ],
            "supporting_transcripts": [
                ev["transcript_id"]
                for ev in system_response.get("evidence_snippets", [])
            ],
            "confidence": system_response.get("confidence", "UNKNOWN")
        }

        self.store.append_turn(
            session_id=session_id,
            turn_context=turn_context
        )
    def get_last_context(self, session_id: str) -> Optional[Dict]:
        return self.store.get_last_turn(session_id)

    def get_full_context(self, session_id: str) -> List[Dict]:
        return self.store.get_session(session_id) or []

    def get_relevant_context(
        self,
        session_id: str,
        current_query: str
    ) -> Optional[Dict]:
        return self.get_last_context(session_id)

    def is_followup_query(self, session_id: str) -> bool:
        return self.get_last_context(session_id) is not None
