import os
import re
import yaml
import torch
import chromadb
from sentence_transformers import SentenceTransformer

# Paths
KB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "knowledge_base"))
DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))

# SOTA Large Model (1.34 GB, 1024 Dimensions)
EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"

def parse_okf_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse YAML frontmatter
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}, content

    yaml_content = match.group(1)
    body = content[match.end():].strip()
    try:
        meta = yaml.safe_load(yaml_content)
        if not isinstance(meta, dict):
            meta = {}
    except Exception:
        meta = {}
    return meta, body

def chunk_document(body):
    # Check if page markers exist (e.g. ## Page 1, ## Page 2, etc.)
    page_splits = re.split(r"##\s+Page\s+(\d+)", body)
    
    chunks = []
    
    # If the document has page markers, we chunk by pages
    if len(page_splits) > 1:
        # page_splits[0] is the text before Page 1 (usually title, intro)
        intro = page_splits[0].strip()
        if intro:
            chunks.append({"text": intro, "page": 1})
            
        for i in range(1, len(page_splits), 2):
            page_num = int(page_splits[i])
            page_content = page_splits[i+1].strip()
            if page_content:
                chunks.append({"text": page_content, "page": page_num})
    else:
        # If no page markers, chunk by paragraphs/sections (approx 1000 characters)
        paragraphs = body.split("\n\n")
        current_chunk = []
        current_len = 0
        
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            
            # If a single paragraph is extremely long, split by sentences or force split
            if len(p) > 1200:
                # Flush current chunk
                if current_chunk:
                    chunks.append({"text": "\n\n".join(current_chunk), "page": 1})
                    current_chunk = []
                    current_len = 0
                chunks.append({"text": p, "page": 1})
            else:
                if current_len + len(p) > 1000:
                    chunks.append({"text": "\n\n".join(current_chunk), "page": 1})
                    current_chunk = [p]
                    current_len = len(p)
                else:
                    current_chunk.append(p)
                    current_len += len(p)
                    
        if current_chunk:
            chunks.append({"text": "\n\n".join(current_chunk), "page": 1})
            
    return chunks

def main():
    # Detect GPU (CUDA)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device detected: {device.upper()}")
    
    print(f"Loading state-of-the-art embedding model: {EMBEDDING_MODEL_NAME}...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME, device=device)
    
    # Initialize Chroma client
    print(f"Initializing Vector Database in: {DB_DIR}")
    chroma_client = chromadb.PersistentClient(path=DB_DIR)
    
    # Create or get collection
    collection = chroma_client.get_or_create_collection(
        name="college_knowledge_base",
        metadata={"hnsw:space": "cosine"}
    )
    
    print("Scanning OKF knowledge base...")
    documents_processed = 0
    
    # Track all chunks first
    ids = []
    documents = []
    metadatas = []
    raw_passages = []
    
    for root, dirs, files in os.walk(KB_DIR):
        for file in files:
            if not file.endswith(".md"):
                continue
            
            file_path = os.path.join(root, file)
            meta, body = parse_okf_file(file_path)
            
            if not body:
                continue
                
            chunks = chunk_document(body)
            rel_path = os.path.relpath(file_path, KB_DIR).replace(os.sep, "/")
            
            for idx, chunk in enumerate(chunks):
                chunk_text = chunk["text"]
                page_num = chunk["page"]
                
                tags_str = ",".join(meta.get("tags", [])) if isinstance(meta.get("tags"), list) else ""
                
                chunk_metadata = {
                    "source": str(meta.get("source", rel_path)),
                    "type": str(meta.get("type", "general_info")),
                    "title": str(meta.get("title", file[:-3])),
                    "tags": tags_str,
                    "page_number": int(page_num),
                    "chunk_index": int(idx),
                    "relative_path": rel_path
                }
                
                chunk_id = f"{rel_path}_chunk_{idx}"
                
                ids.append(chunk_id)
                documents.append(chunk_text)
                metadatas.append(chunk_metadata)
                # BGE model recommends prepending passage: prefix for retrieval keys
                raw_passages.append(f"passage: {chunk_text}")
                
            documents_processed += 1
            if documents_processed % 50 == 0:
                print(f"Scanned {documents_processed} files...")
                
    total_chunks = len(ids)
    print(f"\nScanning completed. Total documents: {documents_processed}. Total chunks: {total_chunks}.")
    
    print(f"Generating embeddings using {device.upper()}...")
    # Generate all embeddings in a single batched call (uses GPU acceleration if device='cuda')
    embeddings_np = model.encode(
        raw_passages,
        batch_size=64 if device == "cuda" else 32,
        show_progress_bar=True,
        normalize_embeddings=True
    )
    embeddings = embeddings_np.tolist()
    
    # Upsert to Chroma DB in batches of 500
    batch_size = 500
    print(f"\nUpserting chunks into Chroma DB...")
    for i in range(0, total_chunks, batch_size):
        end_idx = min(i + batch_size, total_chunks)
        collection.upsert(
            ids=ids[i:end_idx],
            documents=documents[i:end_idx],
            metadatas=metadatas[i:end_idx],
            embeddings=embeddings[i:end_idx]
        )
        print(f"Uploaded batch {i // batch_size + 1}/{(total_chunks + batch_size - 1) // batch_size}...")

    print(f"\nSuccess! Successfully indexed {documents_processed} files into {total_chunks} chunks inside the Vector DB.")

if __name__ == "__main__":
    main()
