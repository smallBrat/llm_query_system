# app/utils/evaluator.py

import os
import requests
from dotenv import load_dotenv

# Load token from .env
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}

def evaluate_via_huggingface_api(query: str, summarized_clause: str):
    prompt = (
        f"Based on the clause below, does it answer the question: '{query}'?\n\n"
        f"Clause: {summarized_clause}\n\n"
        f"Answer with Yes, No or Unknown."
    )

    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    result = response.json()

    try:
        answer = result[0]["summary_text"].strip().split('.')[0].strip()
        brief = answer.split()[0].capitalize()

        if brief not in ["Yes", "No", "Unknown"]:
            brief = "Unknown"
    except:
        print("❌ Evaluation failed:", result)
        brief = "Unknown"

    return {"decision": brief}