"""
Application configuration module.

Uses pydantic-settings to load configuration from environment variables
and .env files. Implements the Singleton pattern via @lru_cache.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        groq_api_key: API key for Groq LLM provider.
        llm_model: Model identifier for the LLM.
        llm_temperature: Temperature for LLM generation.
        llm_max_tokens: Maximum tokens for LLM response.
        embedding_model: Sentence Transformer model name.
        chunk_size: Number of characters per text chunk.
        chunk_overlap: Overlap between consecutive chunks.
        upload_dir: Directory for uploaded files.
        faiss_index_dir: Directory for FAISS indices.
        app_host: Application host address.
        app_port: Application port number.
        log_level: Logging level.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # LLM Configuration
    groq_api_key: str = ""
    llm_model: str = "llama-3.3-70b-versatile"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 2048

    # Embedding Configuration
    embedding_model: str = "BAAI/bge-small-en-v1.5"

    # Chunking Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Storage Configuration
    upload_dir: str = "data/uploads"
    faiss_index_dir: str = "data/faiss_indices"

    # Application Configuration
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"


@lru_cache()
def get_settings() -> Settings:
    """
    Get the application settings singleton.

    Returns:
        Settings: The application settings instance.
    """
    return Settings()
