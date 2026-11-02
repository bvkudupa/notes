import math
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    base_url=os.environ["OPENAI_BASE_URL"]+"/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)

query = "I cannot log in to my account"
candidates = [
    "I am locked out and my password does not work",
    "How do I download my invoice history?",
    "The mobile app crashes when I open the camera",
    "Can I change the email address on my profile?",
    "Your latest update looks really nice"
]

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=[query] + candidates,
)

query_vec = response.data[0].embedding
candidate_vecs = [d.embedding for d in response.data[1:]]

scored = []
for text, vec in zip(candidates, candidate_vecs):
    scored.append({"text": text, "score": round(cosine(query_vec, vec), 3)})

scored.sort(key=lambda item: item["score"], reverse=True)
print(scored)
# for item in scored:
#     print(item["score"], item["text"])

