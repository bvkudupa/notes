from pathlib import Path
import json
from openai import OpenAI
import chromadb
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

lesson_dir = Path(__file__).resolve().parent
eval_set = [
    {
        "question": "How often do passwords have to change?", 
        "right_chunk": "chunk-0",
    },
    {
        "question": "What happens if a laptop fails its encryption check?", 
        "right_chunk": "chunk-1",
    },
    {
        "question": "Can I plug a USB stick into a finance computer?", 
        "right_chunk": "chunk-3",
    },
    {
        "question": "How long does guest wifi last?", 
        "right_chunk": "chunk-4",
    },
    {
        "question": "Where do I report a security incident?", 
        "right_chunk": "chunk-7",
    }
]
chroma = chromadb.PersistentClient(path=lesson_dir.parent/"11-RAG on Chroma"/"ragchroma")
# collection = chroma.list_collections()
# for item in collection:
#     print(f"\nCollection: {item.name}")
#     print(f"\nCollection metadata: {item.metadata}") # --> itpolicy

collection = chroma.get_collection("itpolicy")
hits = 0
array_json = {}
for text in eval_set:
    # print(text["question"], text["right_chunk"])
    q_vector = client.embeddings.create(
        model="text-embedding-3-small", input=text["question"]
    ).data[0].embedding
    results = collection.query(query_embeddings=[q_vector], n_results=2)
    returned_ids = results["ids"][0]
    hit = text["right_chunk"] in returned_ids
    if hit:
        hits += 1
    # print(f"{text['question'][:45]:48} {'HIT' if hit else 'MISS'} {returned_ids}")
    array_json.setdefault("results", []).append({
        "question": text["question"],
        "right_chunk": text["right_chunk"],
        "returned_ids": results["ids"][0],
        "hit": hit
        })
   
# print(f"Hit Rate: {hits}/{len(eval_set)} = {hits/len(eval_set)}")
hit_rate = hits/len(eval_set)
array_json["hit_rate"] = hit_rate

with open(lesson_dir/"rag-output.json", "w") as f:
    json.dump(array_json, f, indent=2)


# print(os.listdir(lesson_dir/"11-RAG on Chroma/ragchroma"))
