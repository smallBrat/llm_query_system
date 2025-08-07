# parser/query_parser.py

from transformers import pipeline
import json

# Load lightweight local model
nlp = pipeline("text2text-generation", model="google/flan-t5-small", max_length=64)

def parse_query(query: str) -> dict:
    prompt = f"Extract intent and key entities in JSON format: {query}"

    try:
        output = nlp(prompt)[0]['generated_text']
        parsed = json.loads(output)
        return parsed
    except Exception:
        # fallback if model doesn't return valid JSON
        return {
            "intent": "general_query",
            "entities": []
        }
