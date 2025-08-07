# app/utils/clause_summarizer.py

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
}

def summarize_clause(text: str, min_length=5, max_length=60) -> str:
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": max_length,
            "min_length": min_length,
            "do_sample": False
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    result = response.json()

    if isinstance(result, list) and "summary_text" in result[0]:
        return result[0]["summary_text"].strip()
    else:
        print("❌ Summarization failed:", result)
        return "Summary generation failed"


def save_summary_to_json(query: str, clause: str, summary: str, file_path="outputs/summarized_results.json"):
    """
    Optional: Save for debugging or offline use
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "original_clause": clause[:500],
        "summary": summary
    }

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(entry)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    print("✅ Summary saved")
