# embed/faiss_store.py
import faiss
import numpy as np

def build_faiss_index(embeddings):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index

def search_faiss(index, query_embedding, top_k=5):
    D, I = index.search(np.array([query_embedding]).astype("float32"), top_k)
    return I[0], D[0]
