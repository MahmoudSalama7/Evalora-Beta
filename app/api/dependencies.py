"""
FastAPI dependency injection providers.

Uses FastAPI's Depends() system to wire up services and
infrastructure components. Implements the Dependency Injection
pattern for loose coupling and testability.
"""

from functools import lru_cache

from app.config import Settings, get_settings
from app.domain.interfaces.llm_provider import LLMProvider
from app.infrastructure.embeddings.sentence_transformer_embeddings import (
    SentenceTransformerEmbeddings,
)
from app.infrastructure.llm.groq_provider import GroqProvider
from app.infrastructure.storage.memory_conversation_repository import (
    MemoryConversationRepository,
)
from app.infrastructure.vectorstore.faiss_repository import FAISSRepository
from app.services.conversation_service import ConversationService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.prompt_service import PromptService
from app.services.qa_service import QAService
from app.services.vector_store_service import VectorStoreService


# ─── Singleton Infrastructure Providers ────────────────────────────

@lru_cache()
def get_embedding_provider() -> SentenceTransformerEmbeddings:
    """Get the singleton embedding provider."""
    settings = get_settings()
    return SentenceTransformerEmbeddings(model_name=settings.embedding_model)


@lru_cache()
def get_llm_provider() -> LLMProvider:
    """Get the singleton LLM provider."""
    settings = get_settings()
    return GroqProvider(
        api_key=settings.groq_api_key,
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )


@lru_cache()
def get_faiss_repository() -> FAISSRepository:
    """Get the singleton FAISS repository."""
    return FAISSRepository()


@lru_cache()
def get_conversation_repository() -> MemoryConversationRepository:
    """Get the singleton conversation repository."""
    return MemoryConversationRepository()


# ─── Service Providers ─────────────────────────────────────────────

@lru_cache()
def get_embedding_service() -> EmbeddingService:
    """Get the singleton embedding service."""
    return EmbeddingService(
        embedding_provider=get_embedding_provider(),
    )


@lru_cache()
def get_vector_store_service() -> VectorStoreService:
    """Get the singleton vector store service."""
    return VectorStoreService(
        vector_repository=get_faiss_repository(),
    )


@lru_cache()
def get_prompt_service() -> PromptService:
    """Get the singleton prompt service."""
    return PromptService()


@lru_cache()
def get_conversation_service() -> ConversationService:
    """Get the singleton conversation service."""
    return ConversationService(
        conversation_repository=get_conversation_repository(),
    )


@lru_cache()
def get_document_service() -> DocumentService:
    """Get the singleton document service."""
    return DocumentService(
        settings=get_settings(),
        embedding_service=get_embedding_service(),
        vector_store_service=get_vector_store_service(),
        llm_provider=get_llm_provider(),
        prompt_service=get_prompt_service(),
    )


@lru_cache()
def get_qa_service() -> QAService:
    """Get the singleton QA service."""
    return QAService(
        embedding_service=get_embedding_service(),
        vector_store_service=get_vector_store_service(),
        prompt_service=get_prompt_service(),
        conversation_service=get_conversation_service(),
        llm_provider=get_llm_provider(),
    )
