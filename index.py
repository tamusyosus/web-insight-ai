"""
embed_index.py

Purpose:
1. Load the SentenceTransformer embedding model.
2. Convert text chunks into vector embeddings.
3. Build a FAISS vector index for similarity search.
"""

import os
import faiss
from sentence_transformers import SentenceTransformer

# Embedding model
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Folder to cache the downloaded model
MODEL_CACHE = os.path.abspath(".cache/models")

# Create the cache folder if it doesn't exist
os.makedirs(MODEL_CACHE, exist_ok=True)


def load_embedder()-> SentenceTransformer:
    """
    Load the SentenceTransformer embedding model.

    Returns:
        SentenceTransformer: Loaded embedding model.
    """

    model = SentenceTransformer(
        EMBED_MODEL,
        cache_folder=MODEL_CACHE
    )

    return model


def create_embeddings(chunks, model):
    """
    Convert text chunks into vector embeddings.

    Parameters:
        chunks (list[str]): List of text chunks.
        model (SentenceTransformer): Loaded embedding model.

    Returns:
        numpy.ndarray: Embedding vectors.
    """

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings.astype("float32")


def build_index(embeddings):
    """
    Build a FAISS vector index.

    Parameters:
        embeddings (numpy.ndarray): Embedding vectors.

    Returns:
        faiss.IndexFlatL2: FAISS vector index.
    """

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index