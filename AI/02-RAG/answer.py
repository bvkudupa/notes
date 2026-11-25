import os
import sys
from pathlib import Path
from openai import OpenAI
import chromadb
from dotenv import load_dotenv

load_dotenv()

lesson_dir = Path(__file__).resolve().parent

text = sys.argv[1]

client = OpenAI()

q_vector = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
).data[0].embedding

chroma = chromadb.PersistentClient(path=lesson_dir/"ragchroma")
collection = chroma.get_collection("itpolicy")
results = collection.query(
    query_embeddings=[q_vector],
    n_results=2
)
top_chunks = results["documents"][0]
docs_text = "\n\n".join(
    f"Document {i+1}: {chunk}" for i, chunk in enumerate(top_chunks)
)
prompt = (
    "Answer the question using only the documents below. If the answer "
    "is not in the documents, say \"The documents do not contain this "
    "information.\"\n\n"
    f"{docs_text}\n\n"
    f"Question: {text}"
)
reply = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
)
print(reply.choices[0].message.content)