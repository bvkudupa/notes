import os
import sys
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv

if len(sys.argv) < 2:
    print('Usage: python ask_doc.py "your question"', file=sys.stderr)
    sys.exit(1)

question = " ".join(sys.argv[1:])
document_path = Path(__file__).with_name("runbook.md")

load_dotenv()
base_url = f"{os.getenv('OPENAI_BASE_URL').rstrip('/')}/v1"

model = ChatOpenAI(model="gpt-4o-mini", base_url=base_url, api_key=os.environ["OPENAI_API_KEY"])

@tool
def read_document(file_path: str) -> str:
    """Read the contents of a file."""
    with open(file_path, 'r') as file:
        return file.read()

agent = create_agent(
    model=model,
    tools=[read_document],
    system_prompt=(
        "Answer questions using only the runbook document. Read the document "
        "before answering. If it does not contain the answer, say you don't know."
    ),
)

answer = agent.invoke({
    "messages": [{
        "role": "user",
        "content": f"Read {document_path} and answer this question: {question}",
    }]
})
print(answer["messages"][-1].content)