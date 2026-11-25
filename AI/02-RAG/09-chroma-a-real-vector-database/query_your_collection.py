
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

lesson_dir = Path(__file__).resolve().parent
database_path = lesson_dir / "chroma_db"

client = OpenAI(
    base_url=os.environ["OPENAI_BASE_URL"].rstrip("/"),
    api_key=os.environ["OPENAI_API_KEY"],
)

question = "How far in advance do I ask for days off?"

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
)

query_vector = response.data[0].embedding

chroma = chromadb.PersistentClient(path=str(database_path))

collection = chroma.get_collection("handbook")

results = collection.query(
    query_embeddings=[query_vector],
    n_results=2
)

for doc, distance in zip(results["documents"][0], results["distances"][0]):
    print(f"Document: {doc}, Distance: {distance:.3f}")