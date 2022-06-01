from typing import Optional

from livearea.entities.sessions import SessionId, Session

SessionMap = dict[SessionId, Session]


class SessionRepository:
    def __init__(self, initial_sessions: Optional[SessionMap] = None) -> None:
        self.sessions: SessionMap = initial_sessions or {}

    async def get(self, session_id: SessionId) -> Session:
        return self.sessions[session_id]

    async def save(self, session: Session) -> None:
        self.sessions[session.id] = session

    async def delete(self, session: Session) -> None:
        del self.sessions[session.id]
