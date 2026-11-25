# Retrieval-augmented generation (RAG)

Follow these eight lessons in order to build a simple RAG workflow, from the
problem it solves to storing and querying your own vectors. Lesson folders keep
the supporting code, data, and screenshots together; this is the chapter's
single README and learning path.

## Learning path

| Step | Lesson | Materials |
| --- | --- | --- |
| 1 | [The Problem RAG Solves](#1-the-problem-rag-solves) | [`ask.py`](./01-the-problem-rag-solves/ask.py) |
| 2 | [Tools You Will Use](#2-tools-you-will-use) | [`call-embedding.py`](./02-tools-you-will-use/call-embedding.py) |
| 3 | [Grounding a Prompt](#3-grounding-a-prompt) | [Lesson folder](./03-grounding-a-prompt/) |
| 4 | [Embeddings](#4-embeddings) | [`embedding.json`](./04-embeddings/embedding.json) |
| 5 | [Measuring Similarity](#5-measuring-similarity) | [`score-pairs.py`](./05-measuring-similarity/score-pairs.py) |
| 6 | [Semantic Search](#6-semantic-search) | [`rank-support-messages.py`](./06-semantic-search/rank-support-messages.py) |
| 7 | [Chunking](#7-chunking) | [`create_chunk.py`](./07-chunking/create_chunk.py), [`data.txt`](./07-chunking/data.txt), [`chunks.json`](./07-chunking/chunks.json) |
| 8 | [Build Your Own Vector Store](#8-build-your-own-vector-store) | [`create_store.py`](./08-build-your-own-vector-store/create_store.py) |

## Before you start

The examples use Python, the OpenAI Python SDK, and `python-dotenv`. From the
repository root, install the packages and configure your API credentials:

```bash
python3 -m pip install openai python-dotenv
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://api.openai.com"
```

`OPENAI_BASE_URL` is optional when using OpenAI directly. For a compatible
provider, set it to that provider's API base URL. Keep credentials out of
source files and commits. Embedding and chat examples make live API requests
and may incur usage charges.

## 1. The Problem RAG Solves

A language model can answer general questions, but it does not automatically
know the contents of your documents or the latest information in your systems.
RAG retrieves relevant text from a source collection and includes that text
when asking the model to answer.

[`ask.py`](./01-the-problem-rag-solves/ask.py) is a starting point: it sends a
question to a chat model. By itself, it does not retrieve evidence. The
following lessons add the pieces needed to provide that evidence.

## 2. Tools You Will Use

The examples use an OpenAI-compatible API for chat and embeddings. The
[`call-embedding.py`](./02-tools-you-will-use/call-embedding.py) example sends
one text to the embeddings endpoint and prints the vector's dimensions and
first few values. An embedding is a list of numbers; the next lessons explain
what it represents and how to use it.

Run examples from the repository root:

```bash
python AI/02-RAG/02-tools-you-will-use/call-embedding.py
```

## 3. Grounding a Prompt

Retrieval only helps if the answer is grounded in the retrieved text. A prompt
can make that requirement explicit:

> Answer the question using only the document below. If the answer is not in
> the document, say "The document does not contain this information."

Provide the relevant document text with the question. This makes it clear
which source the model should use and what to do when the source has no answer.

![Prompt grounding example](./03-grounding-a-prompt/screenshots/image.png)

## 4. Embeddings

An embedding model turns text into a vector. Texts with related meaning tend
to have vectors that are close under a similarity measure. Embeddings can be
created for individual texts or in batches; the saved
[`embedding.json`](./04-embeddings/embedding.json) is an example response.

## 5. Measuring Similarity

Cosine similarity compares two vectors by measuring the angle between them.
For non-zero vectors, values nearer to `1` indicate a more similar direction.
This implementation is used by
[`score-pairs.py`](./05-measuring-similarity/score-pairs.py):

```python
import math

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)
```

The script embeds two related statements and one unrelated statement, then
compares their scores. These visuals accompany the similarity lesson:

![Similarity visual](./05-measuring-similarity/screenshots/image-1.png)
![Similarity visual](./05-measuring-similarity/screenshots/image-2.png)

## 6. Semantic Search

Semantic search embeds a query and a set of candidate texts, scores each
candidate against the query, and sorts the results by score. Unlike keyword
search, it can find related wording even when the query and source use
different words.

[`rank-support-messages.py`](./06-semantic-search/rank-support-messages.py)
demonstrates ranking candidate support messages against a question. The
highest-scoring result is the best semantic match, not a guarantee that it
contains a complete or correct answer.

![Semantic search visual](./06-semantic-search/screenshots/image-3.png)
![Semantic search visual](./06-semantic-search/screenshots/image-4.png)

## 7. Chunking

Documents are split into smaller pieces called chunks before embedding. This
keeps retrieval focused: the model can receive the most relevant passages
rather than an entire long document.

The sample source is [`data.txt`](./07-chunking/data.txt). The script
[`create_chunk.py`](./07-chunking/create_chunk.py) splits it at paragraph
breaks and writes [`chunks.json`](./07-chunking/chunks.json). Run it from any
working directory:

```bash
python AI/02-RAG/07-chunking/create_chunk.py
```

The script uses the source and output files beside itself. For another
document, the basic paragraph split looks like this:

```python
text = open("runbook.txt").read()
chunks = [p.strip() for p in text.split("\n\n") if p.strip()]

for i, chunk in enumerate(chunks):
    print(f"--- chunk {i} ({len(chunk)} chars)")
    print(chunk)
```

After chunking, embed each chunk and keep its text with its vector. Reuse those
vectors for later searches instead of embedding the source documents every
time.

![Chunking visual](./07-chunking/screenshots/image-9.png)
![Chunking visual](./07-chunking/screenshots/image-10.png)
![Chunking visual](./07-chunking/screenshots/image-11.png)
![Chunking visual](./07-chunking/screenshots/image-12.png)

## 8. Build Your Own Vector Store

A vector store keeps each chunk alongside its embedding so that a query can
retrieve matching chunks later. The lesson's
[`create_store.py`](./08-build-your-own-vector-store/create_store.py) example
embeds sample documents and stores their text and vectors in SQLite.

The workflow is:

1. Split source documents into chunks.
2. Embed each chunk and store the text and vector together.
3. Embed an incoming question.
4. Compare the question vector with the stored vectors and retrieve the best
   matches.

The sample screenshots walk through building and querying the store:

![Vector store visual](./08-build-your-own-vector-store/screenshots/image-13.png)
![Vector store visual](./08-build-your-own-vector-store/screenshots/image-14.png)
![Vector store visual](./08-build-your-own-vector-store/screenshots/image-15.png)
![Vector store visual](./08-build-your-own-vector-store/screenshots/image-16.png)

Here is the SQLite storage step with three scheduling notes:

```python
import json
import os
import sqlite3
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
)

docs = [
    "Deploys to production happen every Tuesday at 4pm.",
    "The staging environment resets nightly at midnight.",
    "On-call handover is Friday at 10am.",
]

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=docs,
)

db = sqlite3.connect("demo.db")
db.execute("create table if not exists docs (text TEXT, embedding TEXT)")
for doc, data in zip(docs, response.data):
    db.execute(
        "insert into docs values (?, ?)",
        (doc, json.dumps(data.embedding)),
    )
db.commit()
print("stored", len(docs), "docs")
```

For a question such as "When does new code go live?", embed the question once,
load the stored vectors, and rank them:

```python
import json
import math
import os
import sqlite3
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
)

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)

question = "When does new code go live?"
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=question,
)
query_vec = response.data[0].embedding

db = sqlite3.connect("demo.db")
scored = []
for text, embedding_json in db.execute("select text, embedding from docs"):
    vec = json.loads(embedding_json)
    scored.append({"text": text, "score": round(cosine(query_vec, vec), 3)})

scored.sort(key=lambda item: item["score"], reverse=True)
for item in scored[:2]:
    print(item["score"], item["text"])
```

This is similar to the ranking loop in [semantic search](#6-semantic-search),
but candidate vectors are loaded from SQLite instead of recomputed. The
question and stored documents must use the same embedding model; vectors from
different models do not share a comparable coordinate space.
