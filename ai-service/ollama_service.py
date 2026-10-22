import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_llama(prompt: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]