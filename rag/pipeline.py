from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from openai import OpenAI
from sentence_transformers import SentenceTransformer

from db.get_connection import get_chroma_client
from rag.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, SYSTEM_PROMPT
from rag.prompts import USER_PROMPT_TEMPLATE


LOGGER = logging.getLogger(__name__)
CHROMA_COLLECTION_NAME = "documents_collection"
DEFAULT_TOP_K = 5
QUERY_EMBEDDER: SentenceTransformer | None = None
_OPENAI_CLIENT: OpenAI | None = None


def _get_default_chroma_path() -> str:
    root = Path(__file__).resolve().parents[1]
    return str(root / "db" / "chroma_db")



def _get_query_embedder() -> SentenceTransformer:
    global QUERY_EMBEDDER
    if QUERY_EMBEDDER is None:
        QUERY_EMBEDDER = SentenceTransformer("BAAI/bge-m3")
    return QUERY_EMBEDDER


def _retrieve_documents(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    collection_name: str = CHROMA_COLLECTION_NAME,
) -> List[Dict[str, Any]]:
    client = get_chroma_client(persist_dir=_get_default_chroma_path())
    collection = client.get_collection(name=collection_name)

    query_embedding = np.asarray(
        _get_query_embedder().encode(
            [query],
            normalize_embeddings=True,
        )[0]
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    if not results:
        return []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    ids = results.get("ids", [[]])[0]

    output: List[Dict[str, Any]] = []
    for index, text in enumerate(documents):
        output.append(
            {
                "id": ids[index] if index < len(ids) else None,
                "text": text,
                "metadata": metadatas[index] if index < len(metadatas) else {},
                "distance": distances[index] if index < len(distances) else None,
            }
        )

    return output


def _rerank_documents(query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not documents:
        return documents

    try:
        embedder = _get_query_embedder()
        query_embedding = embedder.encode([query], normalize_embeddings=True)[0]
        document_texts = [document.get("text", "") for document in documents]
        document_embeddings = embedder.encode(document_texts, normalize_embeddings=True)
        scores = np.dot(document_embeddings, query_embedding)
        ranked_indices = np.argsort(-scores)
        return [documents[index] for index in ranked_indices]
    except Exception as exc:  # pragma: no cover
        LOGGER.warning("Reranker failed, continuing with original order: %s", exc)

    return documents


def _format_context(documents: List[Dict[str, Any]]) -> str:
    if not documents:
        return ""

    context_parts: List[str] = []
    for index, document in enumerate(documents, start=1):
        metadata = document.get("metadata") or {}
        source_title = metadata.get("file_name") or metadata.get("ai_title") or metadata.get("file_path") or document.get("id")
        chunk_index = metadata.get("chunk_index")

        header = f"Source {index}: {source_title}"
        if chunk_index is not None:
            header += f" (chunk {chunk_index})"

        context_parts.append(f"{header}\n{document.get('text', '').strip()}")

    return "\n\n---\n\n".join(context_parts)


def _get_openai_client() -> OpenAI:
    global _OPENAI_CLIENT
    if _OPENAI_CLIENT is None:
        _OPENAI_CLIENT = OpenAI(
            base_url=OPENAI_BASE_URL,
            api_key=OPENAI_API_KEY,
        )
    return _OPENAI_CLIENT


def _generate_answer(query: str, context: str) -> str:
    client = _get_openai_client()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT_TEMPLATE.format(query=query, context=context)},
    ]
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
    )
    return (response.choices[0].message.content or "").strip()


def chat(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    rerank: bool = False,
    collection_name: str = CHROMA_COLLECTION_NAME,
) -> Dict[str, Any]:
    """Run a full RAG chat pipeline and return answer metadata."""
    retrieved_documents = _retrieve_documents(
        query=query,
        top_k=top_k,
        collection_name=collection_name,
    )

    rerank_applied = False
    if rerank:
        reranked_documents = _rerank_documents(query, retrieved_documents)
        if reranked_documents is not retrieved_documents:
            rerank_applied = True
        retrieved_documents = reranked_documents

    context = _format_context(retrieved_documents)
    if not retrieved_documents:
        return {
            "query": query,
            "rewritten_query": query,
            "retrieved_documents": [],
            "context": "",
            "answer": "I could not find relevant documents in the vector database.",
            "rerank_applied": rerank_applied,
            "collection_name": collection_name,
            "top_k": top_k,
        }

    final_answer = _generate_answer(query=query, context=context)

    return {
        "query": query,
        "rewritten_query": query,
        "retrieved_documents": retrieved_documents,
        "context": context,
        "answer": final_answer,
        "rerank_applied": rerank_applied,
        "collection_name": collection_name,
        "top_k": top_k,
    }
