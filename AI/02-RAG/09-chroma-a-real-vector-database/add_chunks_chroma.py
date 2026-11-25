import json
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

lesson_dir = Path(__file__).resolve().parent
chunks_path = lesson_dir.parent / "07-chunking" / "chunks.json"
database_path = lesson_dir / "chroma_db"

client = OpenAI(
    base_url=os.environ["OPENAI_BASE_URL"].rstrip("/"),
    api_key=os.environ["OPENAI_API_KEY"],
)

with chunks_path.open("r") as f:
    chunks = json.load(f)

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=chunks,
)

vectors = [data.embedding for data in response.data]

chroma = chromadb.PersistentClient(path=str(database_path))

collection = chroma.get_or_create_collection(name="handbook")
collection.upsert(
    documents=chunks,
    embeddings=vectors,
    ids=[f"chunk-{i}" for i in range(len(chunks))],
)

print("stored:", collection.count())