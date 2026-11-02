# AI Fundamentals

This folder introduces the building blocks behind LLM applications: model
requests, prompts, chains, tools, and agents. Read the sections in order, then
follow the links into each small project to see those ideas applied to files.

## Learning path

| Step | Topic | Example |
| --- | --- | --- |
| 1 | Send a chat request and understand message history | [Chat completions](#1-send-a-chat-request) |
| 2 | Turn a prompt and a model into a reusable chain | [`llm_chain.py`](./llm_chain.py) |
| 3 | Let an agent choose and call a tool | [`llm_agent.py`](./llm_agent.py) |
| 4 | Apply an agent to a document, a log, and support tickets | [Hands-on projects](#4-hands-on-projects) |

## Before you start

The Python examples use LangChain and an OpenAI-compatible chat API. From this
folder, install the packages and provide credentials in your environment or a
`.env` file:

```bash
python3 -m pip install langchain langchain-openai python-dotenv
export OPENAI_API_KEY="your-api-key"
```

`OPENAI_BASE_URL` is optional when using OpenAI directly. For a compatible
provider, set it to that provider's API base URL; the Python examples append
`/v1` when needed. Keep credentials out of source files and commits.

## 1. Send a chat request

A chat request is a sequence of messages with roles such as `user` and
`assistant`. Sending earlier messages along with the latest question gives the
model context from the conversation. The JSON body of a chat-completions
request can look like this:

```json
{
  "model": "your-model-name",
  "messages": [
    {"role": "user", "content": "What is a good tool for formatting JSON?"},
    {"role": "assistant", "content": "jq is a great choice."},
    {"role": "user", "content": "Give me the install command for it."}
  ]
}
```

Send this body to your provider's `/v1/chat/completions` endpoint using its
documented authentication method. Replace `your-model-name` with a model
available from your provider. The important part is the `messages` array: the
model receives the conversation history, not just the final question.

## 2. Build a chain from a prompt and a model

A chain connects reusable steps. In this example, a prompt template provides
the `{topic}` variable and the model generates the response. The `|` operator
passes the formatted prompt to the model.

Run the complete example from this folder:

```bash
python llm_chain.py
```

Open [`llm_chain.py`](./llm_chain.py) to see how it:

- Loads configuration from the environment and `.env`.
- Creates a `ChatOpenAI` model.
- Defines a `ChatPromptTemplate` and pipes it into the model.
- Invokes the chain with a topic and prints the response.

## 3. Give an agent a tool

A chain follows the steps you connect. An agent can decide whether to use one
of its available tools to answer a request. In
[`llm_agent.py`](./llm_agent.py), the `multiply` tool performs arithmetic and
the agent is asked a multiplication question.

```bash
python llm_agent.py
```

Compare this file with [`llm_chain.py`](./llm_chain.py): the chain always runs
the prompt through the model, while the agent can choose to call the tool.

## 4. Hands-on projects

Each project puts an agent in front of a small, local set of files. Run
commands from this folder so the examples can find their project assets.

### Ask questions about a runbook

[`projects/runbook/ask_doc.py`](./projects/runbook/ask_doc.py) defines a
document-reading tool and instructs the agent to answer using the runbook.
The source document is
[`projects/runbook/runbook.md`](./projects/runbook/runbook.md), and both files
are in the [`projects/runbook/` folder](./projects/runbook/).

```bash
python projects/runbook/ask_doc.py "Who owns the reports API?"
```

### Explain a log

[`projects/log-explain/main.py`](./projects/log-explain/main.py) accepts a
question and an optional log-file path. It reads the selected log through a
tool and asks the model to answer from the log evidence. The included sample is
[`projects/log-explain/sample.log`](./projects/log-explain/sample.log); browse
the [`projects/log-explain/ folder`](./projects/log-explain/).

```bash
python projects/log-explain/main.py "Why did the request fail?"
python projects/log-explain/main.py --log-file /path/to/other.log "What happened?"
```

### Triage support tickets

[`projects/support-triage/main.py`](./projects/support-triage/main.py) lists
and reads every `.txt` ticket, then writes a JSON classification for each one.
The example inputs are in
[`projects/support-triage/root/tickets/`](./projects/support-triage/root/tickets/):

- [`reset-password.txt`](./projects/support-triage/root/tickets/reset-password.txt)
- [`double-charge.txt`](./projects/support-triage/root/tickets/double-charge.txt)

The corresponding example results are in
[`projects/support-triage/root/triaged/`](./projects/support-triage/root/triaged/):

- [`reset-password.json`](./projects/support-triage/root/triaged/reset-password.json)
- [`double-charge.json`](./projects/support-triage/root/triaged/double-charge.json)

Run the classifier from this folder:

```bash
python projects/support-triage/main.py
```

The command writes or overwrites the matching JSON files in `root/triaged/`.
Use `--tickets-dir` and `--output-dir` to choose different input and output
folders.

## Where to go next

Continue to [02-RAG](../02-RAG/readme.md) to explore retrieval-augmented
generation, or browse [03-FDE](../03-FDE/readme.md) for the next topic in this
AI learning series.
