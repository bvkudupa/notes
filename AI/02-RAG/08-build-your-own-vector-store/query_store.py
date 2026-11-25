from openai import OpenAI
import os
import sqlite3
import json
import math
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com").rstrip("/"),
    api_key=os.environ["OPENAI_API_KEY"],
)

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)

question = "I removed a file by mistake, can I get it back?"
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=question,
)
query_vec = response.data[0].embedding

db = sqlite3.connect("demo.db")
scored = []
for text, embedding_json in db.execute("select text, embedding from documents"):
    vec = json.loads(embedding_json)
    scored.append({"text": text, "score": round(cosine(query_vec, vec), 3)})

scored.sort(key=lambda item: item["score"], reverse=True)
for item in scored[:2]:
    print(item["score"], item["text"])