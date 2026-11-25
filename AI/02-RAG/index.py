import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import chromadb

load_dotenv()

lesson_dir = Path(__file__).resolve().parent
with open(lesson_dir/"itpolicy.txt", "r") as f:
    text = f.read()

chunks = []
for paragraph in text.split("\n\n"):
    chunks.append(paragraph.strip())

client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL"), api_key=os.environ["OPENAI_API_KEY"])
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=chunks
)

chroma = chromadb.PersistentClient(path=lesson_dir/"ragchroma")
collection = chroma.get_or_create_collection("itpolicy")
collection.add(
    ids = [f"chunk-{i}" for i in range(len(chunks))],
    documents = chunks,
    embeddings=[d.embedding for d in response.data],
)

print("indexed:", collection.count())


