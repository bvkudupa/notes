import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
base_url = f"{os.getenv('OPENAI_BASE_URL').rstrip('/')}/v1"

model = ChatOpenAI(
    model="gpt-4o-mini", #gpt-4o since using the paid key
    base_url=base_url,
    api_key=os.environ["OPENAI_API_KEY"],
)
prompt = ChatPromptTemplate.from_template("Explain {topic} in two sentences.")
chain = prompt | model

reply = chain.invoke({"topic": "what is 4817 times 39?"})

print(reply)