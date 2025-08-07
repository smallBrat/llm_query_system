# app/pipeline.py

import tempfile
import requests
from app.utils.pdf_loader import load_pdf
from app.utils.chunker import chunk_text
from app.utils.embedder import embed_text
from app.utils.faiss_store import build_faiss_index, search_faiss
from app.utils.clause_summarizer import summarize_clause
from app.utils.evaluator import evaluate_via_huggingface_api

def download_pdf(url: str) -> str:
    """Download the PDF from a remote URL and save it locally."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("❌ Failed to download PDF")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        return tmp.name

def process_document_and_questions(doc_url: str, questions: list) -> list:
    """Process the PDF and list of questions to return brief logic-evaluated answers."""
    pdf_path = download_pdf(doc_url)
    text = load_pdf(pdf_path)
    chunks = chunk_text(text)
    chunk_embeddings = embed_text(chunks)
    index = build_faiss_index(chunk_embeddings)

    answers = []

    for query in questions:
        # Embed and retrieve top chunks
        query_embedding = embed_text([query])[0]
        top_indices, _ = search_faiss(index, query_embedding, top_k=3)
        top_chunks = [chunks[i] for i in top_indices]

        # Summarize top chunk
        summary = summarize_clause(top_chunks[0])

        # Evaluate using Hugging Face API
        result = evaluate_via_huggingface_api(query, summary)

        # Append only the final decision: Yes / No / Unknown
        answers.append(result["decision"])

    return answers
