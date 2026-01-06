import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY","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")

API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are a Python programming tutor.\n"
    "Rules:\n"
    "1. Answer ONLY Python-related topics\n"
    "2. Explain in simple language\n"
    "3. ALWAYS include at least one Python code example\n"
    "4. Use correct syntax\n"
    "5. Beginner-friendly\n"
)

def ask_python_topic(topic: str) -> str:
    if not topic or not topic.strip():
        return "Please enter a Python topic."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",   # ✅ use this model (stable & free)
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"Explain the Python topic with example: {topic}"
            }
        ],
        "temperature": 0.3,
        "max_tokens": 600           # ✅ REQUIRED by Groq
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # 🔴 IMPORTANT: print error details if it fails
    if response.status_code != 200:
        return (
            f"Groq API Error {response.status_code}\n\n"
            f"{response.text}"
        )

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
