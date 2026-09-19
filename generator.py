import os
import re
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

def make_context(results):
    return "\n\n".join(
        f"[Source: {r['metadata'].get('source', 'Unknown')}]\n{r['text']}"
        for r in results
    )

def ollama_generate(question, context):
    prompt = f"""
You are a helpful document-grounded AI assistant.

Answer the question using ONLY the supplied context.
Do not invent facts.
If the answer is not contained in the context, clearly say that it is not available in the provided documents.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1}
        },
        timeout=90
    )
    response.raise_for_status()
    answer = response.json().get("response", "").strip()

    if not answer:
        raise RuntimeError("Ollama returned an empty response.")

    return answer

def fallback_generate(question, results):
    if not results:
        return "No relevant information was found in the uploaded documents."

    question_words = {
        word.lower()
        for word in re.findall(r"[A-Za-z0-9]+", question)
        if len(word) > 2
    }

    scored = []

    for result in results:
        sentences = re.split(r"(?<=[.!?])\s+", result["text"])
        for sentence in sentences:
            words = set(re.findall(r"[A-Za-z0-9]+", sentence.lower()))
            score = len(question_words & words)
            if score:
                scored.append((score, sentence.strip()))

    scored.sort(key=lambda x: x[0], reverse=True)

    if not scored:
        return results[0]["text"][:900]

    return " ".join(sentence for _, sentence in scored[:5])

def generate_answer(question, results):
    context = make_context(results)

    try:
        return ollama_generate(question, context), "Ollama LLM"
    except Exception:
        return fallback_generate(question, results), "Local fallback"
