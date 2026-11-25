import os
import json
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com").rstrip("/"),
    api_key=os.environ["OPENAI_API_KEY"],
)

docs = [
   "To reset your password, open Settings then Security and click Reset.",
   "Invoices are emailed on the first of each month.",
   "You can invite teammates from the Members page.",
   "Export your data as CSV from the Reports tab.",
   "Two-factor login is turned on in the Security settings.",
   "Deleted items stay in the trash for 30 days."
]

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=docs
)

db = sqlite3.connect("demo.db")

db.execute(
    """
    CREATE TABLE IF NOT EXISTS docs (
        text TEXT,
        embedding TEXT
    )
    """
)

for doc, data in zip(docs, response.data):
    db.execute(
        "insert into docs values (?, ?)",
        (doc, json.dumps(data.embedding)),
    )
db.commit()
print("stored", len(docs), "docs")

# print(db.execute("select * from docs").fetchall()) 