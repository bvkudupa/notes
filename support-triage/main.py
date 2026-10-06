import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()
base_url = f"{os.getenv('OPENAI_BASE_URL').rstrip('/')}/v1"

@tool
def list_files(directory: str) -> list:
    """List all files in a directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

@tool
def read_file(file_path: str) -> str:
    """Read the contents of a file."""
    with open(file_path, 'r') as file:
        return file.read()

@tool
def write_file(file_path: str, content: str) -> None:
    """Write content to a file."""
    with open(file_path, 'w') as file:
        file.write(content)

model = ChatOpenAI(
    model="gpt-4o-mini", #gpt-4o since using the paid key
    base_url=base_url,
    api_key=os.environ["OPENAI_API_KEY"])

agent = create_agent(
    model=model,
    tools=[list_files, read_file, write_file],
    system_prompt="You are a helpful assistant. Use a tool when you need one.",
)

answer = agent.invoke({"messages": [{"role": "user", "content": "Read every text file from '/Users/udupa/Documents/vscode/notes/root/tickets'. Classify it and return the JSON with fields category and priority. One of the categories is 'billing', technical, account and others and one of the priorities is 'high', low, medium, critical and write them to root/triaged directory as each json file filename should be instead of .txt it should be of .json extension."}]})
print(answer["messages"][-1].text)