import importlib
import unittest
from unittest.mock import MagicMock, patch


class TestRagPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import rag.pipeline as pipeline  # noqa: F401
        cls.pipeline = importlib.reload(importlib.import_module("rag.pipeline"))

    def test_chat_pipeline_returns_structured_response(self):
        with (
            patch("rag.pipeline.get_chroma_client") as mock_get_chroma_client,
            patch("rag.pipeline._get_openai_client") as mock_get_openai_client,
        ):
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "documents": [["first document text", "second document text"]],
                "metadatas": [[
                    {"file_name": "Document 1", "chunk_index": 0},
                    {"file_name": "Document 2", "chunk_index": 1},
                ]],
                "distances": [[0.1, 0.2]],
                "ids": [["id-1", "id-2"]],
            }
            mock_client = MagicMock()
            mock_client.get_collection.return_value = mock_collection
            mock_get_chroma_client.return_value = mock_client

            mock_openai = MagicMock()
            mock_openai.chat.completions.create.return_value = MagicMock(
                choices=[MagicMock(message=MagicMock(content="final answer"))]
            )
            mock_get_openai_client.return_value = mock_openai

            result = self.pipeline.chat("what is the campus wifi password?", top_k=2)

            self.assertEqual(result["query"], "what is the campus wifi password?")
            self.assertEqual(result["rewritten_query"], "what is the campus wifi password?")
            self.assertEqual(result["answer"], "final answer")
            self.assertEqual(result["top_k"], 2)
            self.assertFalse(result["rerank_applied"])
            self.assertEqual(len(result["retrieved_documents"]), 2)
            self.assertIn("Source 1: Document 1", result["context"])
            self.assertIn("Source 2: Document 2", result["context"])
            mock_openai.chat.completions.create.assert_called_once()
            call_kwargs = mock_openai.chat.completions.create.call_args.kwargs
            self.assertEqual(call_kwargs["model"], "llama-rag")
            self.assertEqual(call_kwargs["messages"][0]["role"], "system")

    def test_chat_pipeline_applies_rerank_when_enabled(self):
        with (
            patch("rag.pipeline.get_chroma_client") as mock_get_chroma_client,
            patch("rag.pipeline._get_query_embedder") as mock_get_query_embedder,
            patch("rag.pipeline._get_openai_client") as mock_get_openai_client,
        ):
            original_docs = [
                {"id": "id-1", "text": "first", "metadata": {"file_name": "Document 1", "chunk_index": 0}, "distance": 0.1},
                {"id": "id-2", "text": "second", "metadata": {"file_name": "Document 2", "chunk_index": 1}, "distance": 0.2},
            ]
            mock_collection = MagicMock()
            mock_collection.query.return_value = {
                "documents": [["first", "second"]],
                "metadatas": [[original_docs[0]["metadata"], original_docs[1]["metadata"]]],
                "distances": [[0.1, 0.2]],
                "ids": [["id-1", "id-2"]],
            }
            mock_client = MagicMock()
            mock_client.get_collection.return_value = mock_collection
            mock_get_chroma_client.return_value = mock_client

            mock_openai = MagicMock()
            mock_embedder = MagicMock()
            mock_embedder.encode.side_effect = [
                __import__("numpy").array([[1.0, 0.0]]),
                __import__("numpy").array([[1.0, 0.0]]),
                __import__("numpy").array([[0.1, 0.9], [0.9, 0.1]]),
            ]
            mock_get_query_embedder.return_value = mock_embedder

            mock_openai.chat.completions.create.return_value = MagicMock(
                choices=[MagicMock(message=MagicMock(content="final answer"))]
            )
            mock_get_openai_client.return_value = mock_openai

            result = self.pipeline.chat("how do I register for classes?", rerank=True)

            self.assertTrue(result["rerank_applied"])
            self.assertEqual(result["retrieved_documents"][0]["id"], "id-2")
            self.assertEqual(result["retrieved_documents"][1]["id"], "id-1")


if __name__ == "__main__":
    unittest.main()
