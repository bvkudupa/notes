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