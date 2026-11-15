import os
import json

with open("AI/02-RAG/data.txt", "r") as file:
    text = file.read()

# print(text.split("\n\n"))

# for p in text.split("\n\n"):
#     print(p.strip())

chunks = [p.strip() for p in text.split("\n\n") if p.strip()]

# chunks_json = json.dumps(chunks, indent=4)
# for i, chunk in enumerate(chunks):
#      print(f"--- chunk {i} ({len(chunk)} chars)")
#      print(chunk)

with open("AI/02-RAG/chunks.json", "w") as file:
    json.dump(chunks, file, indent=4)