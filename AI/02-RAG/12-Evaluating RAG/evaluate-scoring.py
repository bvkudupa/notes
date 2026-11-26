from openai import OpenAI
from dotenv import load_dotenv
import chromadb
from pathlib import Path
import json

lesson_dir = Path(__file__).resolve().parent

load_dotenv()

text = """
"How often do passwords have to change?" - answer must contain "Monday"
"How often are laptops checked for encryption?" - must contain "90"
"How long does guest wifi access last?" - must contain "24"
"How fast must a security incident be reported?" - must contain "hour"
"How do I book a meeting room?" - must contain "not contain" (the refusal - the policy says nothing about meeting rooms)
"""

eval_set = []

for line in text.splitlines():
    if line.strip() == "":
        continue

    parts = line.split(" - ")

    question = parts[0].strip('"')
    answer_rule = parts[1]

    must_contain = answer_rule.split('"')[1]

    item = {
        "question": question,
        "must_contain": must_contain
    }

    eval_set.append(item)

client = OpenAI()

chroma = chromadb.PersistentClient(path=lesson_dir.parent/"11-RAG on Chroma"/"ragchroma")
collection = chroma.get_collection("itpolicy")


def rag_answer(question):
    q_vector = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    ).data[0].embedding

    top = collection.query(query_embeddings=[q_vector], n_results=2)["documents"][0]
    docs_text = "\n\n".join(f"Document {i+1}: {chunk}" for i, chunk in enumerate(top))
    # print(docs_text)
    prompt = (
    "Answer the question using only the below documents. "
    "If the documents don't contain the answer, say "
    "\"The documents do not contain this information.\"\n\n"
    f"{docs_text}\n\nQuestion: {question}"
    )

    
    reply = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return reply.choices[0].message.content

correct = 0

answer_evaluation = {
    "results": []
}

for test in eval_set:
    answer = rag_answer(test["question"])
    ok = test["must_contain"].lower() in answer.lower()
    if ok:
        correct += 1
    # print(f"{test['question'][:45]:48} {"PASS" if ok else "FAIL"} ")
    item = {
        "question": test["question"],
        "must_contain": test["must_contain"],
        "answer": answer,
        "pass": "PASS" if ok else "FAIL"

    }

    answer_evaluation["results"].append(item)
    

print(f"Answer accuracy {correct}/{len(eval_set)} = {correct/len(eval_set)}")
acc = correct/len(eval_set)
answer_evaluation["accuracy"] = acc

with open(lesson_dir/"answer-eval.json", "w") as f:
    json.dump(answer_evaluation, f, indent=4)
