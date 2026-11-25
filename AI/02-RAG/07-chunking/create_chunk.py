import json
from pathlib import Path

lesson_dir = Path(__file__).resolve().parent

with (lesson_dir / "data.txt").open("r") as file:
    text = file.read()

# print(text.split("\n\n"))

# for p in text.split("\n\n"):
#     print(p.strip())

chunks = [p.strip() for p in text.split("\n\n") if p.strip()]

# chunks_json = json.dumps(chunks, indent=4)
# for i, chunk in enumerate(chunks):
#      print(f"--- chunk {i} ({len(chunk)} chars)")
#      print(chunk)

with (lesson_dir / "chunks.json").open("w") as file:
    json.dump(chunks, file, indent=4)