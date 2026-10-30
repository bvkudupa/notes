import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com").rstrip("/") + "/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="I was charged twice for my invoice",
)

vector = response.data[0].embedding
print(len(vector), vector[:5])