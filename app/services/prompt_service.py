"""
Prompt service.

Constructs structured prompts for the LLM including system
instructions, retrieved context, conversation history,
and the current question.
"""

import logging

from app.domain.models import Message, MessageRole, RetrievalResult

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a precise and helpful document question-answering assistant.

CRITICAL RULES:
1. Answer ONLY using the provided document context below. Do NOT use any external knowledge.
2. If the answer cannot be found in the context, respond with: "I couldn't find this information in the uploaded document." (or its precise translation in the language of the user's question).
3. Be concise but thorough in your answers.
4. When referencing information, mention the page number if available.
5. Maintain a professional and helpful tone.
6. Answer in the same language as the user's question.
7. If the question is ambiguous, acknowledge it and provide the best interpretation based on the context."""

FOLLOW_UP_PROMPT = """

Based on your answer, suggest exactly 3 brief follow-up questions the user might want to ask about this document. Format them as a numbered list on separate lines, prefixed with "FOLLOW_UP:" like:
FOLLOW_UP: 1. [question]
FOLLOW_UP: 2. [question]
FOLLOW_UP: 3. [question]"""

SUMMARY_SYSTEM_PROMPT = """You are a document summarization assistant. Provide a concise summary (3-5 sentences) of the following document content. Focus on the main topics, purpose, and key points of the document."""


class PromptService:
    """
    Service for constructing LLM prompts.

    Builds structured prompts that combine system instructions,
    retrieved document context, conversation history, and the
    user's question to produce grounded answers.
    """

    def build_qa_prompt(
        self,
        question: str,
        retrieved_chunks: list[RetrievalResult],
        conversation_history: list[Message] | None = None,
    ) -> tuple[str, str]:
        """
        Build a question-answering prompt with context.

        Args:
            question: The user's question.
            retrieved_chunks: Relevant chunks from the vector store.
            conversation_history: Previous messages in the conversation.

        Returns:
            A tuple of (system_message, user_prompt).
        """
        # Build context section
        context_parts: list[str] = []
        for i, result in enumerate(retrieved_chunks, 1):
            chunk = result.chunk
            context_parts.append(
                f"[Chunk {i} | Page {chunk.page_number}]\n{chunk.content}"
            )

        context_text = "\n\n---\n\n".join(context_parts)

        # Build conversation history section
        history_text = ""
        if conversation_history:
            history_parts: list[str] = []
            # Include last 6 messages to keep context manageable
            recent_history = conversation_history[-6:]
            for msg in recent_history:
                role_label = "User" if msg.role == MessageRole.HUMAN else "Assistant"
                history_parts.append(f"{role_label}: {msg.content}")
            history_text = (
                "\n\nPrevious Conversation:\n" + "\n".join(history_parts)
            )

        # Construct the user prompt
        user_prompt = f"""Document Context:
{context_text}
{history_text}

Current Question: {question}
{FOLLOW_UP_PROMPT}"""

        logger.debug(
            f"Built QA prompt: {len(retrieved_chunks)} chunks, "
            f"{len(conversation_history or [])} history messages"
        )

        return SYSTEM_PROMPT, user_prompt

    def build_summary_prompt(self, text: str) -> tuple[str, str]:
        """
        Build a document summarization prompt.

        Args:
            text: The document text to summarize.

        Returns:
            A tuple of (system_message, user_prompt).
        """
        # Truncate if very long to stay within token limits
        max_chars = 8000
        truncated = text[:max_chars] if len(text) > max_chars else text

        user_prompt = f"Document Content:\n\n{truncated}"

        return SUMMARY_SYSTEM_PROMPT, user_prompt

    @staticmethod
    def parse_follow_up_questions(response: str) -> tuple[str, list[str]]:
        """
        Extract follow-up questions from the LLM response.

        Args:
            response: The full LLM response text.

        Returns:
            A tuple of (clean_answer, follow_up_questions).
        """
        lines = response.strip().split("\n")
        answer_lines: list[str] = []
        follow_ups: list[str] = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("FOLLOW_UP:"):
                question = stripped.replace("FOLLOW_UP:", "").strip()
                # Remove leading numbering
                if question and question[0].isdigit() and ". " in question:
                    question = question.split(". ", 1)[1]
                if question:
                    follow_ups.append(question)
            else:
                answer_lines.append(line)

        clean_answer = "\n".join(answer_lines).strip()
        return clean_answer, follow_ups
