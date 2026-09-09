"""
Production-ready ingestion pipeline template.

NOTE:
This file is an upgraded version of the user's script. It intentionally keeps
the structure simple while introducing:
- Recursive DFS via Path.rglob()
- RecursiveCharacterTextSplitter
- Explicit BAAI/bge-m3 embeddings
- vLLM OpenAI-compatible metadata endpoint placeholder
- Metadata enrichment before embedding
- metadata_log.jsonl logging
- Batched embedding
- ChromaDB explicit embeddings

Install:
pip install chromadb sentence-transformers langchain-text-splitters pdfplumber python-docx requests tqdm
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path

import chromadb
import docx
import pdfplumber
import requests
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm

# ---------------- CONFIG ----------------

EMBED_MODEL = "BAAI/bge-m3"
VLLM_URL = "http://localhost:8000/v1/chat/completions"
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

SUPPORTED = {".pdf",".docx",".md",".txt"}

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=120,
)

embedder = SentenceTransformer(
    EMBED_MODEL,
    device="cuda"
)

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("documents_collection")


def sha(path):
    h = hashlib.sha256()
    with open(path,"rb") as f:
        while True:
            b=f.read(1024*1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def extract(path:Path):
    if path.suffix.lower()==".pdf":
        txt=[]
        with pdfplumber.open(path) as pdf:
            for p in pdf.pages:
                t=p.extract_text()
                if t:
                    txt.append(t)
        return "\n".join(txt)

    if path.suffix.lower()==".docx":
        d=docx.Document(path)
        return "\n".join(x.text for x in d.paragraphs if x.text.strip())

    return path.read_text(encoding="utf8",errors="ignore")


def metadata(text):

    prompt=f"""Return ONLY JSON:
{{
"title":"",
"document_type":"",
"summary":"",
"keywords":[]
}}

Document:
{text}
"""

    payload={
        "model":MODEL_NAME,
        "messages":[
            {"role":"system","content":"Return JSON only."},
            {"role":"user","content":prompt}
        ],
        "temperature":0
    }

    try:
        r=requests.post(VLLM_URL,json=payload,timeout=120)
        data=r.json()["choices"][0]["message"]["content"]
        return json.loads(data)
    except Exception:
        return {
            "title":"Unknown",
            "document_type":"Unknown",
            "summary":text[:300],
            "keywords":[]
        }


def append_log(folder,meta,file,chunks):

    log=Path(folder)/"metadata_log.jsonl"

    with open(log,"a",encoding="utf8") as f:
        f.write(json.dumps({
            "time":datetime.now().isoformat(),
            "file":file.name,
            "path":str(file),
            "title":meta["title"],
            "document_type":meta["document_type"],
            "summary":meta["summary"],
            "keywords":meta["keywords"],
            "chunks":chunks
        })+"\n")


def ingest(folder):

    folder=Path(folder)

    files=[
        x for x in folder.rglob("*")
        if x.is_file() and x.suffix.lower() in SUPPORTED
    ]

    print(f"Found {len(files)} files")

    for file in tqdm(files):

        text=extract(file)

        if not text.strip():
            continue

        meta=metadata(text)

        chunks=splitter.split_text(text)

        append_log(folder,meta,file,len(chunks))

        docs=[]
        ids=[]
        metas=[]

        for i,c in enumerate(chunks):

            enriched=f"""
                    Title:
                    {meta["title"]}

                    Document Type:
                    {meta["document_type"]}

                    Summary:
                    {meta["summary"]}

                    Keywords:
                    {meta["keywords"]}

                    Content:
                    {c}
                    """

            docs.append(enriched)

            metas.append({
                "file":file.name,
                "path":str(file),
                "chunk":i,
                "hash":sha(file),
                "title":meta["title"],
                "document_type":meta["document_type"]
            })

            ids.append(f'{sha(file)}_{i}')

        emb=embedder.encode(
            docs,
            batch_size=64,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        collection.add(
            ids=ids,
            documents=docs,
            embeddings=emb.tolist(),
            metadatas=metas
        )

    print("Finished")


if __name__=="__main__":
    ingest("document/daiict_documents raw")