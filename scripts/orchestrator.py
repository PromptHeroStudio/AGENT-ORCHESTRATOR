import os
import json
from datetime import datetime

import requests
from openai import OpenAI

GROQ_KEY = os.environ["GROQ_API_KEY"]
GEMINI_KEYS = [
    os.environ.get("GEMINI_API_KEY_1", ""),
    os.environ.get("GEMINI_API_KEY_2", ""),
    os.environ.get("GEMINI_API_KEY_3", ""),
]
SANITY_TOKEN = os.environ["SANITY_API_TOKEN"]
SANITY_PROJECT = os.environ["SANITY_PROJECT_ID"]
SANITY_DATASET = os.environ.get("SANITY_DATASET", "production")

REGISTRY_PATH = "Commander/agents/_registry.json"
AGENTS_DIR = "Commander/agents"

groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_KEY,
)


def call_groq(prompt):
    resp = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content


def call_gemini(prompt, key_index=0):
    key = GEMINI_KEYS[key_index]
    if not key:
        raise ValueError(f"GEMINI_API_KEY_{key_index + 1} nije postavljen")
    client = OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=key,
    )
    resp = client.chat.completions.create(
        model="gemini-3.8-flash",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content


def smart_call(prompt):
    try:
        print("\u2192 Poku\u0161avam Groq (llama3-70b-8192)...")
        return call_groq(prompt)
    except Exception as e:
        print(f"Groq pao: {e}")

    for i in range(len(GEMINI_KEYS)):
        if not GEMINI_KEYS[i]:
            continue
        try:
            print(f"\u2192 Poku\u0161avam Gemini #{i + 1}...")
            return call_gemini(prompt, i)
        except Exception as e:
            print(f"Gemini #{i + 1} pao: {e}")

    raise RuntimeError("Svi provajderi su pali.")


def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        return {"agents": []}
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def route_task(task):
    agents = load_registry().get("agents", [])
    if not agents:
        return None
    t = task.lower()
    for agent in agents:
        for kw in agent.get("trigger_keywords", []):
            if kw.lower() in t:
                return agent
    return agents[0]


def write_to_sanity(task, result):
    url = f"https://{SANITY_PROJECT}.api.sanity.io/v2024-01-01/data/mutate/{SANITY_DATASET}"
    headers = {
        "Authorization": f"Bearer {SANITY_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"mutations": [{"create": {
        "_type": "agentResult",
        "task": task,
        "result": result,
        "_createdAt": datetime.utcnow().isoformat() + "Z",
    }}]}
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    if r.status_code >= 400:
        print(f"Sanity gre\u0161ka {r.status_code}: {r.text}")
        r.raise_for_status()
    print(f"Upisano u Sanity: {r.status_code}")


if __name__ == "__main__":
    with open("task.md", "r", encoding="utf-8") as f:
        task = f.read().strip()

    if not task:
        print("task.md je prazan.")
        exit(0)

    print(f"Zadatak: {task[:200]}...")

    agent = route_task(task)
    if agent:
        print(f"\u2192 Rutirano na: @{agent['slug']} ({agent['name']})")
        charter_path = os.path.join(AGENTS_DIR, f"{agent['slug']}.md")
        charter = ""
        if os.path.exists(charter_path):
            with open(charter_path, "r", encoding="utf-8") as f:
                charter = f.read()
    else:
        print("\u2192 Nema registry-ja, koristim generi\u010dki pristup")
        agent = {"slug": "general", "name": "General"}
        charter = ""

    full_prompt = f"""Ti si @{agent['slug']} ({agent['name']}).

Tvoja povelja:
{charter}

Zadatak:
{task}

VA\u017dNO:
- Direktno izvr\u0161i zadatak. NE vra\u0107aj @oznake.
- Vrati SAMO kona\u010dni rezultat, bez ponavljanja zadatka.
- Pi\u0161i na srpskom/hrvatskom jeziku."""

    result = smart_call(full_prompt)
    print(f"Rezultat: {result[:300]}...")

    with open("output.md", "w", encoding="utf-8") as f:
        f.write(result)

    try:
        write_to_sanity(task, result)
    except Exception as e:
        print(f"Sanity upis nije uspeo: {e}")

    print("Gotovo.")
