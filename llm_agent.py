import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()
base_url = f"{os.getenv('OPENAI_BASE_URL').rstrip('/')}/v1"

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the result."""
    return a * b

model = ChatOpenAI(model="gpt-4o-mini", base_url=base_url, api_key=os.environ["OPENAI_API_KEY"])

agent = create_agent(
    model=model,
    tools=[multiply],
    system_prompt="You are a helpful assistant. Use a tool when you need one.",
)

answer = agent.invoke({"messages": [{"role": "user", "content": "What is 4817 times 39?"}]})
print(answer["messages"][-1].text)