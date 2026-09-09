"""RAG orchestration package.

This package exposes a single public entrypoint for the retrieval-augmented
chat pipeline.
"""

from .pipeline import chat

__all__ = ["chat"]
