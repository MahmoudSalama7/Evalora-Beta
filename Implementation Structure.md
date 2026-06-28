# Walkthrough — DocuMind AI: PDF/DOCX QA Assistant

## What Was Built

A **production-ready RAG-based Question Answering Assistant** for legal documents, comprising ~45 files across a clean layered architecture.

---

## Deliverables

| # | Deliverable | File(s) |
|---|---|---|
| 1 | Complete source code | [app/](file:///d:/INTRV/app) — 25 Python files across 4 layers |
| 2 | requirements.txt | [requirements.txt](file:///d:/INTRV/requirements.txt) |
| 3 | Dockerfile | [Dockerfile](file:///d:/INTRV/Dockerfile) — Multi-stage build with model pre-download |
| 4 | docker-compose.yml | [docker-compose.yml](file:///d:/INTRV/docker-compose.yml) |
| 5 | README.md | [README.md](file:///d:/INTRV/README.md) — Architecture diagrams, API docs, examples |
| 6 | .env.example | [.env.example](file:///d:/INTRV/.env.example) |
| 7 | Unit tests | [tests/](file:///d:/INTRV/tests) — 22 tests, all passing |
| 8 | Frontend UI | [frontend/](file:///d:/INTRV/frontend) — Dark-themed glassmorphism chat interface |

---

## Architecture Summary

```
API Layer (FastAPI routes)
    ↓ Depends()
Service Layer (business logic orchestration)
    ↓
Infrastructure Layer (concrete adapters)
    ↓
Domain Layer (pure Python entities + interfaces)
```

### Design Patterns Implemented

| Pattern | Location | Purpose |
|---|---|---|
| **Factory** | [parser_factory.py](file:///d:/INTRV/app/infrastructure/parsers/parser_factory.py) | Auto-select PDF/DOCX parser by extension |
| **Strategy** | [groq_provider.py](file:///d:/INTRV/app/infrastructure/llm/groq_provider.py) | Swappable LLM backends |
| **Repository** | [faiss_repository.py](file:///d:/INTRV/app/infrastructure/vectorstore/faiss_repository.py) | Abstract vector DB from business logic |
| **Dependency Injection** | [dependencies.py](file:///d:/INTRV/app/api/dependencies.py) | FastAPI Depends() for loose coupling |
| **Singleton** | [config.py](file:///d:/INTRV/app/config.py) | `@lru_cache` settings instance |

### Key Technical Decisions

- **Groq** (not OpenAI) as LLM provider per user request, using `llama-3.3-70b-versatile`
- **In-memory** FAISS and conversation storage (lightest option per user preference)
- **One document per chat session** (per user requirement)
- **Open API** (no authentication)
- **SSE streaming** for real-time token delivery to the frontend

---

## RAG Pipeline Flow

```
Document Upload → PyMuPDF/python-docx Parse → RecursiveCharacterTextSplitter (1000/200)
    → BAAI/bge-small-en-v1.5 Embeddings → FAISS IndexFlatIP (cosine similarity)

Question → Query Embedding → FAISS Top-K Search → Similarity Threshold Gate (0.25)
    → Prompt Construction (system + context + history + question)
    → Groq LLM Generation → Follow-up Question Parsing → Response
```

---

## Test Results

✅ **22/22 tests passed** in 10.29s

| Test File | Tests | Status |
|---|---|---|
| [test_api.py](file:///d:/INTRV/tests/test_api.py) | 10 (health, upload, chat, stream, history, errors) | ✅ |
| [test_chunking.py](file:///d:/INTRV/tests/test_chunking.py) | 1 (page metadata, indices) | ✅ |
| [test_embedding_service.py](file:///d:/INTRV/tests/test_embedding_service.py) | 1 (batch + query) | ✅ |
| [test_parsers.py](file:///d:/INTRV/tests/test_parsers.py) | 5 (factory, PDF, DOCX, registration) | ✅ |
| [test_prompt_service.py](file:///d:/INTRV/tests/test_prompt_service.py) | 2 (prompt building, follow-up parsing) | ✅ |
| [test_qa_service.py](file:///d:/INTRV/tests/test_qa_service.py) | 2 (happy path, threshold gate) | ✅ |
| [test_vector_repository.py](file:///d:/INTRV/tests/test_vector_repository.py) | 1 (FAISS index + search + delete) | ✅ |

---

## How to Run

### Local Development
```bash
cd d:\INTRV
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```
Then open `http://localhost:8000`

### Docker
```bash
docker compose up --build
```

### Run Tests
```bash
.\venv\Scripts\python -m pytest tests/ -v
```

---

## Stretch Goals Completed

- ✅ Streaming token responses (SSE)
- ✅ Conversation history (per session)
- ✅ Docker support (Dockerfile + docker-compose.yml)
- ✅ Source citations (page, chunk, score, preview)
- ✅ Automatic document summary after upload
- ✅ Suggested follow-up questions
- ✅ Modern premium UI with glassmorphism dark theme
