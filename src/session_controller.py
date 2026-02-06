import uuid
from typing import Dict, Optional

from context_store import ContextStore
from context_manager import ContextManager


class SessionController:
    def __init__(self):
        self.context_store = ContextStore()
        self.context_manager = ContextManager(self.context_store)
        self.session_id: Optional[str] = None
    def get_or_create_session(self) -> str:
        if self.session_id is None:
            self.session_id = str(uuid.uuid4())
            self.context_store.create_session(self.session_id)
        return self.session_id
    def prepare_request(self, user_query: str) -> Dict:
        session_id = self.get_or_create_session()

        prior_context = self.context_manager.get_relevant_context(
            session_id=session_id,
            current_query=user_query
        )

        return {
            "session_id": session_id,
            "current_query": user_query,
            "prior_context": prior_context
        }
    def store_result(self, user_query: str, system_result: Dict):
        session_id = self.get_or_create_session()

        self.context_manager.update_context(
            session_id=session_id,
            user_query=user_query,
            system_response=system_result
        )
