from __future__ import annotations

import os


OPENAI_BASE_URL = os.getenv("RAG_OPENAI_BASE_URL", "http://localhost:8000/v1")
OPENAI_API_KEY = os.getenv("RAG_OPENAI_API_KEY", "local-api-key")
OPENAI_MODEL = os.getenv("RAG_OPENAI_MODEL", "llama-rag")

SYSTEM_PROMPT = (
    "You are an expert assistant. Answer the user's question using only the "
    "provided context. If the answer is not contained in the context, say "
    "that you do not know."
)
