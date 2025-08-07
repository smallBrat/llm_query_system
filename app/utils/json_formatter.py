# output/json_formatter.py
import json

def format_output(query, matched_clause, decision, confidence):
    return {
        "query": query,
        "matched_clause": matched_clause,
        "decision": decision,
        "confidence": float(confidence)
    }
