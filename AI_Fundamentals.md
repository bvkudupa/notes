# 1
curl -s "$OPENAI_BASE_URL/v1/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "minimax-m3", "messages": [
    {"role": "user", "content": "What is a good tool for formatting JSON on the command line?"},
    {"role": "assistant", "content": "jq is a great choice."},
    {"role": "user", "content": "Give me the install command for it."}
  ]}' \
  | jq -r '.choices[0].message.content'

Model	Rough character	Reach for it when
deepseek-v4-flash	Fast, cheap, general	You want a quick, solid answer to an everyday request
deepseek-v4-pro	Deeper reasoning, slower	The problem has several steps or needs careful thinking
glm-5.2	Strong all-rounder	You want a capable general model and aren't sure which to pick
gpt-oss-120b	Large open model	You want extra capacity from a big model and can wait a little
minimax-m3	Quick and concise	You want short, to-the-point replies at speed

# 2
mkdir -p /root/tools
curl -s "$OPENAI_BASE_URL/v1/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-v4-pro", "messages": [{"role": "user", "content": "What is the weather in Paris right now?"}],
    "tools": [{"type": "function", "function": {
      "name": "get_weather",
      "description": "Get the current weather for a city",
      "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}
    }}]}' > /root/tools/weather-call.json

# 3 Setup Github MCP server
echo "GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here" >> /root/.env
source /root/.env
export GITHUB_PERSONAL_ACCESS_TOKEN

claude mcp add github -e GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_PERSONAL_ACCESS_TOKEN -- npx -y @modelcontextprotocol/server-github
claude mcp list

node.js is the backend for running the Java script

node somejavascript.js to run the JS

npm install downlaods, npx it downloads to cache and runs it.. (it downloads from npm registry)


# 4 Run below command on fresh server
pip3 install --break-system-packages --ignore-installed openai anthropic
python3 -c "import openai, anthropic; print('ready')"


# 5 Py

# cat ask.py 
import sys
import openai

client = openai.OpenAI()

reply = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[{"role": "user", "content": sys.argv[1]}],
)
print(reply.choices[0].message.content)
# cat ask_claude_style.py 
import anthropic

client = anthropic.Anthropic()

reply = client.messages.create(
    model="minimax-m3",
    max_tokens=2000,
    messages=[{"role": "user", "content": "What is a container, in two sentences?"}],
)
print(reply.content[0].text)

# 6

import glob, os, openai

client = openai.OpenAI()
os.makedirs("/root/summaries", exist_ok=True)

for path in glob.glob("/root/inbox/*.txt"):
    text = open(path).read()
    reply = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[{"role": "user", "content": f"Summarize this in a sentence:\n\n{text}"}],
    )
    out = "/root/summaries/" + os.path.basename(path)
    open(out, "w").write(reply.choices[0].message.content)

# 7
Three jobs show up in almost every LLM app, and LangChain gives each one a reusable piece:

- The API call. A chat model object talks to the API for you. You call it like a function and get the reply text back, instead of hand-building JSON and parsing it.
- The prompt. A prompt template is a string with holes in it. You write the wording once with a variable like {topic}, then fill the hole with a real value each time. No more gluing strings together.
- The chaining. You pipe the template into the model so the filled-in prompt flows straight into the call as one unit. That combined unit is a "chain", which is where the name comes from.

# Chat model
LangChain's OpenAI-compatible model lives in the langchain-openai package and is called ChatOpenAI. It reads the same two environment variables you've been using all along - OPENAI_BASE_URL for the API URL and OPENAI_API_KEY for the key - so you don't paste either into your code. You only pick which model answers:
```
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-oss-120b")
```

# Top free LLM
- deepseek-v4-flash
- deepseek-v4-pro
- glm-5.2
- gpt-oss-120b
- minimax-m3

# The prompt template

```
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "Explain what is {topic} in two sentences"
)
```

# Piping them into a chain
The | operator joins the pieces so the filled-in prompt flows into the model as one unit. Call .invoke() with the variables and read the reply off the result:

```chain = prompt | model
reply = chain.invoke({"topic": "DNS"})
print(reply.content)
```

# Langchain example

```
mport os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

model = ChatOpenAI(
    model="glm-5.2",
    base_url=os.environ["OPENAI_BASE_URL"] + "/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)
prompt = ChatPromptTemplate.from_template("Explain {topic} in two sentences.")
chain = prompt | model

reply = chain.invoke({"topic": "how DNS resolves a domain name"})

import pathlib
pathlib.Path("/root/langchain-lab").mkdir(exist_ok=True)
pathlib.Path("/root/langchain-lab/output.txt").write_text(reply.content)
```





