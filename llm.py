import ollama, json, re

MODEL = "gemma4:e2b"   # <--- CHANGE THIS to exactly what `ollama list` shows

def extract(text):
    prompt = f"""Extract durable memories and entities from this message.

Message: "{text}"

Return JSON only:
{{"memories": [{{"text": "...", "kind": "fact|preference|task|decision", "entities": ["name1", "name2"]}}]}}

Rules:
- 1 to 3 memories max.
- Each memory is a short standalone sentence.
- Entities are people, projects, tools, dates, or topics mentioned."""
    try:
        r = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}], format="json")
        data = json.loads(r["message"]["content"])
        out = []
        for m in data.get("memories", []):
            names = []
            for e in m.get("entities", []):
                names.append(e.get("name", "") if isinstance(e, dict) else str(e))
            out.append({"text": m.get("text", ""), "kind": m.get("kind", "fact"),
                        "entities": [n for n in names if n]})
        if out:
            return {"memories": out}
    except Exception as e:
        print(f"[llm] extract fallback ({e})")
    caps = list(dict.fromkeys(re.findall(r"\b[A-Z][a-zA-Z0-9]+\b", text)))
    return {"memories": [{"text": text, "kind": "fact", "entities": caps[:5]}]}

def answer(question, memories):
    if not memories:
        return "No shared memories available yet."
    ctx = "\n".join(f"[{m['id']}] (by {m['agent']}, {m['kind']}) {m['text']}" for m in memories)
    prompt = f"""You are an AI agent with shared persistent memory.
Answer the question using ONLY the memories below.
Cite memory IDs in square brackets like [abc123]. If memories do not contain the answer, say so.

Memories:
{ctx}

Question: {question}

Answer:"""
    r = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return r["message"]["content"].strip()