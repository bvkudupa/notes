import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()
base_url = f"{os.getenv('OPENAI_BASE_URL').rstrip('/')}/v1"

@tool
def read_path(file_path: str) -> str:
    """Read the contents of a file."""
    with open(file_path, 'r') as file:
        return file.read()

model = ChatOpenAI(model="gpt-4o-mini", base_url=base_url, api_key=os.environ["OPENAI_API_KEY"])

agent = create_agent(model=model, tools=[read_path], system_prompt="You are an experienced site reliability engineer. Use a tool when you need one")

answer = agent.invoke({"messages": [{"role": "user", "content": "Read the file from '/Users/udupa/Documents/vscode/notes/log-explain/sample.log' and one or two sentences of summary of what happened and the most likely cause"}]})
print(answer["messages"][-1].text)
