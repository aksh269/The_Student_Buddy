# The-Student-Buddy

Chat agent for students.

## How To Run

1. Start the local vLLM server on `cuda:0`:

```bash
CUDA_VISIBLE_DEVICES=0 vllm serve NousResearch/Meta-Llama-3-8B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --dtype auto \
  --gpu-memory-utilization 0.82 \
  --max-model-len 2048 \
  --served-model-name llama-rag
```

2. Run a single RAG query:

```bash
python run_rag_chat.py "what are the requirement of msc data science program"
```

The default OpenAI-compatible endpoint is `http://localhost:8000/v1`, and the model name used by the app is `llama-rag`.

## Architecture Overview

- `rag/pipeline.py` implements the RAG flow. It embeds the user query, retrieves top documents from Chroma, optionally reranks them, formats context, and asks the local vLLM server for the final answer.
- `db/get_connection.py` and the Chroma database under `db/chroma_db` provide vector retrieval over the indexed academic documents.
- `rag/config.py` holds the OpenAI-compatible base URL, API key, model name, and system prompt used by the chat pipeline.
- `run_rag_chat.py` is the CLI entrypoint for a single user query and prints the structured JSON response.

The data flow is: user query -> embedding retrieval -> reranking -> context assembly -> local vLLM chat completion -> JSON output.
