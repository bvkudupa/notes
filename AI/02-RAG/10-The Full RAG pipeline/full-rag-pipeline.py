import math
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

lesson_dir = Path(__file__).resolve().parent
output_dir = lesson_dir / "outputs"
output_dir.mkdir(exist_ok=True)

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.environ["OPENAI_API_KEY"],
)


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    len_a = math.sqrt(sum(x * x for x in a))
    len_b = math.sqrt(sum(y * y for y in b))
    return dot / (len_a * len_b)


# Phase 1: index the handbook (run once before answering questions).
docs = [
    "Release notes are published on the team wiki every Friday afternoon.",
    "The test suite must pass before any branch is merged to main.",
    "Production alerts page the on-call engineer through the paging app.",
    "New services need a security review before their first deploy.",
]

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=docs,
)
vectors = [data.embedding for data in response.data]


def retrieve(question):
    # Phase 2: embed the question and retrieve the closest document.
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question,
    )
    query_vector = response.data[0].embedding

    best_score = -1.0
    best_doc = None

    for doc, vector in zip(docs, vectors):
        similarity = cosine_similarity(query_vector, vector)
        print(f"{similarity:.3f} {doc}")
        if similarity > best_score:
            best_score = similarity
            best_doc = doc

    if best_doc is None:
        raise RuntimeError("No document was available to retrieve.")

    print("Retrieved:", best_doc)
    return best_doc


def generate_answer(question, document):
    # Phase 3: generate an answer grounded only in the retrieved document.
    prompt = (
        "Answer the question using only the document below. If the answer "
        'is not in the document, say "The document does not contain this '
        'information."\n\n'
        f"Document: {document}\n\n"
        f"Question: {question}"
    )
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    answer = response.choices[0].message.content
    if answer is None:
        raise RuntimeError("The chat model returned no answer.")
    return answer


questions = [
    "Where do the release notes get published?",
    "What is the wifi password in the office?",
]

for index, question in enumerate(questions, start=1):
    print(f"\nQuestion: {question}")
    document = retrieve(question)
    answer = generate_answer(question, document)

    if index == 1:
        (output_dir / "retrieved.txt").write_text(document + "\n")
    (output_dir / f"answer-{index}.txt").write_text(answer + "\n")
    print("Answer:", answer)
