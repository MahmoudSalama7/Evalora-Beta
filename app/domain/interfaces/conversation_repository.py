"""
Abstract conversation repository interface.

Defines the contract for conversation persistence,
implementing the Repository Pattern.
"""

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.models import Conversation, Message


class ConversationRepository(ABC):
    """
    Abstract base class for conversation storage.

    Manages the persistence of chat sessions including
    message history and session metadata.
    """

    @abstractmethod
    def create_session(self, session_id: str, document_id: str) -> Conversation:
        """
        Create a new conversation session.

        Args:
            session_id: Unique identifier for the session.
            document_id: ID of the document being discussed.

        Returns:
            The newly created conversation.
        """
        ...

    @abstractmethod
    def get_session(self, session_id: str) -> Optional[Conversation]:
        """
        Retrieve a conversation session.

        Args:
            session_id: The session ID to retrieve.

        Returns:
            The conversation if found, None otherwise.
        """
        ...

    @abstractmethod
    def add_message(self, session_id: str, message: Message) -> None:
        """
        Add a message to an existing conversation.

        Args:
            session_id: The session to add the message to.
            message: The message to add.

        Raises:
            KeyError: If the session_id does not exist.
        """
        ...

    @abstractmethod
    def get_history(self, session_id: str) -> list[Message]:
        """
        Get the message history for a session.

        Args:
            session_id: The session ID to retrieve history for.

        Returns:
            Ordered list of messages in the conversation.

        Raises:
            KeyError: If the session_id does not exist.
        """
        ...

    @abstractmethod
    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists.

        Args:
            session_id: The session ID to check.

        Returns:
            True if the session exists.
        """
        ...
