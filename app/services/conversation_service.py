"""
Conversation service.

Manages chat session lifecycle, message storage,
and conversation history retrieval.
"""

import logging
import uuid

from app.domain.interfaces.conversation_repository import ConversationRepository
from app.domain.models import Conversation, Message, MessageRole

logger = logging.getLogger(__name__)


class ConversationService:
    """
    Service for managing conversation sessions.

    Handles session creation, message persistence,
    and history retrieval.

    Args:
        conversation_repository: The concrete conversation storage.
    """

    def __init__(self, conversation_repository: ConversationRepository) -> None:
        self._repository = conversation_repository

    def get_or_create_session(
        self,
        document_id: str,
        session_id: str | None = None,
    ) -> str:
        """
        Get an existing session or create a new one.

        Args:
            document_id: The document being discussed.
            session_id: Optional existing session ID.

        Returns:
            The session ID (existing or newly created).
        """
        if session_id and self._repository.session_exists(session_id):
            logger.debug(f"Using existing session: {session_id}")
            return session_id

        new_session_id = session_id or str(uuid.uuid4())
        self._repository.create_session(new_session_id, document_id)
        logger.info(f"Created new session: {new_session_id}")
        return new_session_id

    def add_human_message(self, session_id: str, content: str) -> None:
        """
        Record a human message in the conversation.

        Args:
            session_id: The session to add the message to.
            content: The message text.
        """
        message = Message(role=MessageRole.HUMAN, content=content)
        self._repository.add_message(session_id, message)

    def add_assistant_message(self, session_id: str, content: str) -> None:
        """
        Record an assistant message in the conversation.

        Args:
            session_id: The session to add the message to.
            content: The message text.
        """
        message = Message(role=MessageRole.ASSISTANT, content=content)
        self._repository.add_message(session_id, message)

    def get_history(self, session_id: str) -> list[Message]:
        """
        Get the conversation history for a session.

        Args:
            session_id: The session ID.

        Returns:
            List of messages in chronological order.

        Raises:
            KeyError: If the session does not exist.
        """
        return self._repository.get_history(session_id)

    def get_session(self, session_id: str) -> Conversation | None:
        """
        Get a conversation session.

        Args:
            session_id: The session ID.

        Returns:
            The conversation or None if not found.
        """
        return self._repository.get_session(session_id)

    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists."""
        return self._repository.session_exists(session_id)
