"""
History API route.

Handles retrieval of conversation history for a given session.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_conversation_service
from app.api.schemas import ErrorResponse, HistoryResponse, MessageSchema
from app.services.conversation_service import ConversationService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["History"])


@router.get(
    "/history/{session_id}",
    response_model=HistoryResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Session not found"},
    },
    summary="Get conversation history",
    description="Retrieve the conversation history for a session.",
)
async def get_history(
    session_id: str,
    conversation_service: ConversationService = Depends(
        get_conversation_service
    ),
) -> HistoryResponse:
    """
    Retrieve the conversation history for a given session ID.

    Returns all messages in chronological order.
    """
    conversation = conversation_service.get_session(session_id)
    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {session_id}",
        )

    messages = [
        MessageSchema(
            role=msg.role.value,
            content=msg.content,
            timestamp=msg.timestamp,
        )
        for msg in conversation.messages
    ]

    return HistoryResponse(
        session_id=conversation.session_id,
        document_id=conversation.document_id,
        messages=messages,
    )
