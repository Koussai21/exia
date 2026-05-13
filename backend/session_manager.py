import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict
from .models import SessionData, Requirement, ReformulationResult


class SessionManager:
    def __init__(self, ttl_hours: int = 24):
        self.sessions: Dict[str, SessionData] = {}
        self.ttl_hours = ttl_hours

    def create_session(self, filename: str, requirements: list) -> str:
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        now = datetime.now()

        req_objects = [
            Requirement(
                id=r.get("id"),
                nom=r.get("nom"),
                contenu=r.get("contenu"),
                doublon_probable=r.get("doublon_probable", False),
                complexity_score=r.get("complexity_score", 1)
            )
            for r in requirements
        ]

        self.sessions[session_id] = SessionData(
            session_id=session_id,
            filename=filename,
            requirements=req_objects,
            created_at=now,
            updated_at=now
        )
        return session_id

    def get_session(self, session_id: str) -> Optional[SessionData]:
        if session_id not in self.sessions:
            return None

        session = self.sessions[session_id]
        age = datetime.now() - session.created_at

        if age > timedelta(hours=self.ttl_hours):
            del self.sessions[session_id]
            return None

        return session

    def update_reformulations(self, session_id: str, reformulations: Dict[str, ReformulationResult]) -> bool:
        session = self.get_session(session_id)
        if not session:
            return False

        session.reformulations = reformulations
        session.updated_at = datetime.now()
        self.sessions[session_id] = session
        return True

    def delete_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def cleanup_expired(self):
        now = datetime.now()
        expired = [
            sid for sid, session in self.sessions.items()
            if now - session.created_at > timedelta(hours=self.ttl_hours)
        ]
        for sid in expired:
            del self.sessions[sid]
        return len(expired)
