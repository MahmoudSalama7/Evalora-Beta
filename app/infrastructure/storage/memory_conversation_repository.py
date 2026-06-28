"""
In-memory conversation repository implementation.

Implements the ConversationRepository interface using
a thread-safe in-memory dictionary for lightweight operation.
"""

import logging
import threading
from typing import Optional

from app.domain.interfaces.conversation_repository import ConversationRepository
from app.domain.models import Conversation, Message

logger = logging.getLogger(__name__)


class MemoryConversationRepository(ConversationRepository):
    """
    Concrete conversation repository using in-memory storage.

    Thread-safe implementation using a lock for concurrent access.
    Data does not persist across server restarts.

    Repository Pattern: Abstracts conversation storage from business logic.
    """

    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}
        self._lock = threading.Lock()

    def create_session(self, session_id: str, document_id: str) -> Conversation:
        """
        Create a new conversation session.

        Args:
            session_id: Unique identifier for the session.
            document_id: ID of the document being discussed.

        Returns:
            The newly created conversation.
        """
        with self._lock:
            conversation = Conversation(
                session_id=session_id,
                document_id=document_id,
            )
            self._conversations[session_id] = conversation
            logger.info(
                f"Created conversation session: {session_id} "
                f"for document: {document_id}"
            )
            return conversation

    def get_session(self, session_id: str) -> Optional[Conversation]:
        """
        Retrieve a conversation session.

        Args:
            session_id: The session ID to retrieve.

        Returns:
            The conversation if found, None otherwise.
        """
        with self._lock:
            return self._conversations.get(session_id)

    def add_message(self, session_id: str, message: Message) -> None:
        """
        Add a message to an existing conversation.

        Args:
            session_id: The session to add the message to.
            message: The message to add.

        Raises:
            KeyError: If the session_id does not exist.
        """
        with self._lock:
            if session_id not in self._conversations:
                raise KeyError(f"Session not found: {session_id}")

            self._conversations[session_id].messages.append(message)
            logger.debug(
                f"Added {message.role.value} message to session {session_id}"
            )

    def get_history(self, session_id: str) -> list[Message]:
        """
        Get the message history for a session.

        Args:
            session_id: The session ID.

        Returns:
            Ordered list of messages.

        Raises:
            KeyError: If the session_id does not exist.
        """
        with self._lock:
            if session_id not in self._conversations:
                raise KeyError(f"Session not found: {session_id}")

            return list(self._conversations[session_id].messages)

    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists."""
        with self._lock:
            return session_id in self._conversations
