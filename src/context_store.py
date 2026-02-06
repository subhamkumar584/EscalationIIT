from typing import Dict, List, Optional


class ContextStore:
    def __init__(self):
        self.sessions: Dict[str, List[Dict]] = {}
    def create_session(self, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []

    def reset_session(self, session_id: str):
        self.sessions[session_id] = []

    def append_turn(self, session_id: str, turn_context: Dict):
        if session_id not in self.sessions:
            self.create_session(session_id)

        self.sessions[session_id].append(turn_context)

    def get_session(self, session_id: str) -> Optional[List[Dict]]:
        return self.sessions.get(session_id)

    def get_last_turn(self, session_id: str) -> Optional[Dict]:
        history = self.sessions.get(session_id)
        if not history:
            return None
        return history[-1]
