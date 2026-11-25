import os
import math
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.environ["OPENAI_BASE_URL"].rstrip("/") + "/v1",
    api_key=os.environ["OPENAI_API_KEY"],

)

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)

sentences = [
    "The server ran out of disk space overnight",
    "Storage on the machine filled up during the night",
    "The new logo looks great on the website",
]

response = client.embeddings.create(model="text-embedding-3-small", input=sentences)
vectors = [d.embedding for d in response.data]
print("vectors:", len(vectors), "dim:", len(vectors[0]))
# print(response.data)
# for d in response.data:
#     print(d.embedding)
similar = cosine(vectors[0], vectors[1])
unrelated = cosine(vectors[0], vectors[2])


print("similar:", round(similar, 3), " unrelated:", round(unrelated, 3))