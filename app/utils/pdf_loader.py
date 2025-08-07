# ingest/pdf_loader.py
import fitz  # PyMuPDF

def load_pdf(path):
    doc = fitz.open(path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text
