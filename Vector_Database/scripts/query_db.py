import os
import sys
import torch
import chromadb
from sentence_transformers import SentenceTransformer

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))
EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/query_db.py \"<your search query>\" [filter_type]")
        sys.argv = [sys.argv[0], "hostel rules"] # Default search query for testing
        print(f"No query provided. Running default query: '{sys.argv[1]}'\n")
        
    query_text = sys.argv[1]
    filter_type = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Detect device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device detected: {device.upper()}")
    
    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME, device=device)
    
    print(f"Connecting to Vector Database in: {DB_DIR}")
    chroma_client = chromadb.PersistentClient(path=DB_DIR)
    
    try:
        collection = chroma_client.get_collection("college_knowledge_base")
    except Exception:
        print("Error: Collection 'college_knowledge_base' not found. Please build the database first.")
        return

    # Generate query embedding
    print(f"Generating query embedding for: '{query_text}'...")
    # BGE models recommend query prefix
    query_passage = f"query: {query_text}"
    query_embedding = model.encode(query_passage, normalize_embeddings=True).tolist()
    
    # Configure filters
    where_filter = {}
    if filter_type:
        where_filter["type"] = filter_type
        print(f"Applying metadata filter: type = '{filter_type}'")
        
    # Query database
    print("Searching vector database...")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        where=where_filter if where_filter else None
    )
    
    print("\n--- Search Results ---")
    if not results or not results["documents"] or len(results["documents"][0]) == 0:
        print("No results found.")
        return
        
    for i in range(len(results["documents"][0])):
        doc = results["documents"][0][i]
        meta = results["metadatas"][0][i]
        dist = results["distances"][0][i]
        
        print(f"\nResult #{i+1} [Similarity Score: {1 - dist:.4f}]")
        print(f"Title: {meta.get('title')}")
        print(f"Type: {meta.get('type')}")
        print(f"Source: {meta.get('source')}")
        print(f"Page: {meta.get('page_number', 'N/A')}")
        print(f"Tags: {meta.get('tags')}")
        print("-" * 40)
        print(doc.strip())
        print("-" * 40)

if __name__ == "__main__":
    main()
