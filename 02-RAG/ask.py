import os
import sys
from dotenv import load_dotenv

from openai import OpenAI

text = sys.argv[1]
load_dotenv()

client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com").rstrip("/") + "/v1",
    api_key=os.environ.get("OPENAI_API_KEY"),
)

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": f"{text}"
        }
    ],
)

print(response.choices[0].message.content)