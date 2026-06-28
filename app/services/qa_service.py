"""
Question answering service.

Orchestrates the RAG pipeline: query embedding, retrieval,
prompt construction, LLM generation, and response formatting.
"""

import logging
from collections.abc import AsyncIterator

from app.domain.interfaces.llm_provider import LLMProvider
from app.domain.models import AnswerResult, Message
from app.services.conversation_service import ConversationService
from app.services.embedding_service import EmbeddingService
from app.services.prompt_service import PromptService
from app.services.vector_store_service import VectorStoreService

logger = logging.getLogger(__name__)

# Minimum similarity score threshold for retrieval
SIMILARITY_THRESHOLD = 0.25


class QAService:
    """
    Service for question answering using RAG.

    Implements the complete retrieval-augmented generation pipeline:
    1. Embed the query
    2. Retrieve relevant chunks from vector store
    3. Build a grounded prompt with context and history
    4. Generate an answer via LLM
    5. Parse follow-up suggestions
    6. Store conversation messages

    Args:
        embedding_service: Service for generating query embeddings.
        vector_store_service: Service for similarity search.
        prompt_service: Service for prompt construction.
        conversation_service: Service for conversation management.
        llm_provider: LLM for generating answers.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store_service: VectorStoreService,
        prompt_service: PromptService,
        conversation_service: ConversationService,
        llm_provider: LLMProvider,
    ) -> None:
        self._embedding_service = embedding_service
        self._vector_store_service = vector_store_service
        self._prompt_service = prompt_service
        self._conversation_service = conversation_service
        self._llm_provider = llm_provider

    async def answer(
        self,
        document_id: str,
        question: str,
        session_id: str | None = None,
    ) -> AnswerResult:
        """
        Answer a question using the RAG pipeline.

        Args:
            document_id: The document to query.
            question: The user's question.
            session_id: Optional conversation session ID.

        Returns:
            AnswerResult with answer text, sources, and follow-up suggestions.

        Raises:
            KeyError: If the document_id does not exist.
            RuntimeError: If the LLM fails.
        """
        if not self._vector_store_service.document_exists(document_id):
            raise KeyError(f"Document not found: {document_id}")

        logger.info(
            f"Answering question for document {document_id}",
            extra={"document_id": document_id},
        )

        # Step 1: Get or create conversation session
        actual_session_id = self._conversation_service.get_or_create_session(
            document_id=document_id,
            session_id=session_id,
        )

        # Step 2: Embed the query
        query_embedding = self._embedding_service.embed_query(question)

        # Step 3: Retrieve relevant chunks
        results = self._vector_store_service.search(
            document_id=document_id,
            query_embedding=query_embedding,
        )

        # Step 4: Check similarity threshold
        if not results or results[0].score < SIMILARITY_THRESHOLD:
            not_found_msg = (
                "I couldn't find this information in the uploaded document."
            )
            self._conversation_service.add_human_message(
                actual_session_id, question
            )
            self._conversation_service.add_assistant_message(
                actual_session_id, not_found_msg
            )
            return AnswerResult(
                answer=not_found_msg,
                sources=[],
                suggested_questions=[],
            )

        # Step 5: Get conversation history
        history: list[Message] = []
        try:
            history = self._conversation_service.get_history(actual_session_id)
        except KeyError:
            pass

        # Step 6: Build prompt
        system_msg, user_prompt = self._prompt_service.build_qa_prompt(
            question=question,
            retrieved_chunks=results,
            conversation_history=history,
        )

        # Step 7: Generate answer
        raw_response = await self._llm_provider.generate(
            prompt=user_prompt,
            system_message=system_msg,
        )

        # Step 8: Parse follow-up questions
        answer_text, follow_ups = PromptService.parse_follow_up_questions(
            raw_response
        )

        # Step 9: Store conversation
        self._conversation_service.add_human_message(
            actual_session_id, question
        )
        self._conversation_service.add_assistant_message(
            actual_session_id, answer_text
        )

        return AnswerResult(
            answer=answer_text,
            sources=results,
            suggested_questions=follow_ups,
        )

    async def answer_stream(
        self,
        document_id: str,
        question: str,
        session_id: str | None = None,
    ) -> AsyncIterator[dict]:
        """
        Stream an answer using the RAG pipeline via SSE.

        Yields dictionaries with event data for SSE formatting.

        Args:
            document_id: The document to query.
            question: The user's question.
            session_id: Optional conversation session ID.

        Yields:
            Dicts with 'type' and 'data' keys for SSE events.
        """
        if not self._vector_store_service.document_exists(document_id):
            yield {
                "type": "error",
                "data": f"Document not found: {document_id}",
            }
            return

        # Get or create session
        actual_session_id = self._conversation_service.get_or_create_session(
            document_id=document_id,
            session_id=session_id,
        )

        # Embed query
        query_embedding = self._embedding_service.embed_query(question)

        # Retrieve chunks
        results = self._vector_store_service.search(
            document_id=document_id,
            query_embedding=query_embedding,
        )

        # Check threshold
        if not results or results[0].score < SIMILARITY_THRESHOLD:
            not_found_msg = (
                "I couldn't find this information in the uploaded document."
            )
            self._conversation_service.add_human_message(
                actual_session_id, question
            )
            self._conversation_service.add_assistant_message(
                actual_session_id, not_found_msg
            )
            yield {"type": "token", "data": not_found_msg}
            yield {"type": "done", "data": ""}
            return

        # Emit sources first
        sources_data = [
            {
                "page": r.chunk.page_number,
                "chunk": r.chunk.chunk_index,
                "score": round(r.score, 4),
                "preview": r.chunk.content[:100] + "...",
            }
            for r in results
        ]
        yield {"type": "sources", "data": sources_data}

        # Get history and build prompt
        history: list[Message] = []
        try:
            history = self._conversation_service.get_history(actual_session_id)
        except KeyError:
            pass

        system_msg, user_prompt = self._prompt_service.build_qa_prompt(
            question=question,
            retrieved_chunks=results,
            conversation_history=history,
        )

        # Stream response
        full_response = ""
        try:
            async for token in self._llm_provider.stream(
                prompt=user_prompt,
                system_message=system_msg,
            ):
                full_response += token
                yield {"type": "token", "data": token}
        except Exception as exc:
            logger.error(f"Streaming failed: {exc}", exc_info=True)
            yield {"type": "error", "data": str(exc)}
            return

        # Parse follow-ups and store conversation
        answer_text, follow_ups = PromptService.parse_follow_up_questions(
            full_response
        )

        self._conversation_service.add_human_message(
            actual_session_id, question
        )
        self._conversation_service.add_assistant_message(
            actual_session_id, answer_text
        )

        if follow_ups:
            yield {"type": "follow_ups", "data": follow_ups}

        yield {
            "type": "done",
            "data": {"session_id": actual_session_id},
        }
