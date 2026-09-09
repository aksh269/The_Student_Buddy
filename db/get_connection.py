# db/chroma.py

from pathlib import Path
import chromadb
from chromadb.config import Settings


def get_chroma_client(
    persist_dir: str = "UniAsist/db/chroma_db",
):
    """
    Returns a persistent ChromaDB client.

    Args:
        persist_dir: Directory where the Chroma database is stored.

    Returns:
        chromadb.PersistentClient
    """
    Path(persist_dir).parent.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(
        path=persist_dir,
        settings=Settings(
            anonymized_telemetry=False
        )
    )

    return client
