import os
from datetime import datetime

import requests
from openai import OpenAI

# ── Konfiguracija (čita se iz GitHub Secrets) ─────────────────
GROQ_KEY = os.environ["GROQ_API_KEY"]
GEMINI_KEYS = [
    os.environ.get("GEMINI_API_KEY_1", ""),
    os.environ.get("GEMINI_API_KEY_2", ""),
]
SANITY_TOKEN = os.environ["SANITY_API_TOKEN"]
SANITY_PROJECT = os.environ["SANITY_PROJECT_ID"]
SANITY_DATASET = os.environ.get("SANITY_DATASET", "production")

# ── Groq klijent (OpenAI-kompatibilan endpoint) ───────────────
groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_KEY,
)


def call_groq(prompt: str) -> str:
    """Primarni LLM poziv — Groq. Brz i besplatan tier."""
    resp = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content


def call_gemini(prompt: str, key_index: int = 0) -> str:
    """Fallback — Gemini preko OpenAI-kompatibilnog endpoint-a."""
    key = GEMINI_KEYS[key_index]
    if not key:
        raise ValueError(f"GEMINI_API_KEY_{key_index + 1} nije postavljen")
    client = OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=key,
    )
    resp = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content


def smart_call(prompt: str) -> str:
    """Fallback lanac: Groq → Gemini #1 → Gemini #2."""
    try:
        print("→ Pokušavam Groq (llama-3.3-70b-versatile)...")
        return call_groq(prompt)
    except Exception as e:
        print(f"Groq pao: {e}")

    for i in range(len(GEMINI_KEYS)):
        try:
            print(f"→ Pokušavam Gemini #{i + 1} (gemini-2.0-flash)...")
            return call_gemini(prompt, i)
        except Exception as e:
            print(f"Gemini #{i + 1} pao: {e}")

    raise RuntimeError("Svi provajderi su pali. Proverite ključeve i limite.")


def write_to_sanity(task: str, result: str) -> None:
    """Upisuje rezultat u Sanity kao dokument tipa agentResult."""
    url = (
        f"https://{SANITY_PROJECT}.api.sanity.io"
        f"/v2024-01-01/data/mutate/{SANITY_DATASET}"
    )
    headers = {
        "Authorization": f"Bearer {SANITY_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "mutations": [
            {
                "create": {
                    "_type": "agentResult",
                    "task": task,
                    "result": result,
                    "_createdAt": datetime.utcnow().isoformat() + "Z",
                }
            }
        ]
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    if r.status_code >= 400:
        print(f"Sanity greška {r.status_code}: {r.text}")
        r.raise_for_status()
    print(f"Upisano u Sanity: {r.status_code}")


# ── Glavni tok ────────────────────────────────────────────────
if __name__ == "__main__":
    with open("task.md", "r", encoding="utf-8") as f:
        task = f.read().strip()

    if not task:
        print("task.md je prazan. Preskačem.")
        exit(0)

    print(f"Zadatak: {task[:200]}...")

    rules = ""
    if os.path.exists("Commander/rules.md"):
        with open("Commander/rules.md", "r", encoding="utf-8") as f:
            rules = f.read()

    full_prompt = f"""Ti si orkestrator AI agenata. Sledeća pravila važe:

{rules}

Korisnikov zadatak:
{task}

Izvrši zadatak i vrati rezultat."""

    result = smart_call(full_prompt)
    print(f"Rezultat: {result[:300]}...")

    # Sačuvaj u repo (GitHub Actions će ovo komitovati nazad)
    with open("output.md", "w", encoding="utf-8") as f:
        f.write(result)

    # Upis u Sanity (ako padne, ne rušimo ceo workflow)
    try:
        write_to_sanity(task, result)
    except Exception as e:
        print(f"Sanity upis nije uspeo: {e}")

    print("Gotovo.")
