import os
import numpy as np
import torch

from scraper import load_webpages
from chunk import chunk_words
from index import (
    load_embedder,
    create_embeddings,
    build_index
)

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline
)

# ------------------------------------------
# Configuration
# ------------------------------------------


# Folder used to store downloaded AI models
MODEL_CACHE = os.path.abspath(".cache/models")

# Language model used to generate answers
GEN_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

# ------------------------------------------
# Build Complete RAG Pipeline
# ------------------------------------------

def build_pipeline(urls: list[str]) -> dict:

    """
        Build the complete RAG pipeline from a list of webpage URLs.

        Steps:
        1. Download webpages.
        2. Chunk the text.
        3. Load embedding model.
        4. Generate embeddings.
        5. Build FAISS index.
        6. Load language model.
        7. Return all pipeline components.
    """
     

    # --------------------------------------
    # Download webpages
    # --------------------------------------

    print("\nDownloading webpages...\n")

    texts, sources = load_webpages(urls)

    # --------------------------------------
    # Chunk webpages
    # --------------------------------------

    chunks = []
    chunk_sources = []

    for text, source in zip(texts, sources):

        page_chunks = chunk_words(
            text,
            chunk_size=500,
            overlap=50
        )

        chunks.extend(page_chunks)

        chunk_sources.extend([source] * len(page_chunks))

    print(f"Total chunks created: {len(chunks)}")

    # --------------------------------------
    # Load embedding model
    # --------------------------------------

    print("\nLoading embedding model...")

    embedder = load_embedder()

    # --------------------------------------
    # Create embeddings
    # --------------------------------------

    print("Creating embeddings...")

    embeddings = create_embeddings( chunks,embedder)

    # --------------------------------------
    # Build FAISS index
    # --------------------------------------

    print("Building FAISS index...")

    index = build_index(embeddings)

    # --------------------------------------
    # Load language model
    # --------------------------------------

    print("Loading language model...")

    tokenizer = AutoTokenizer.from_pretrained(
        GEN_MODEL,
        cache_dir=MODEL_CACHE
    )

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        GEN_MODEL,
        cache_dir=MODEL_CACHE,
        device_map="cuda",
        dtype=torch.float16
    )

    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer
    )

    print("\nPipeline Ready!\n")

    # --------------------------------------
    # Return everything
    # --------------------------------------

    return {
        "chunks": chunks,
        "sources": chunk_sources,
        "embedder": embedder,
        "index": index,
        "generator": generator
    }


# ------------------------------------------
# Retrieve Relevant Chunks
# ------------------------------------------

def retrieve(query, embedder, index, chunks, sources, k=3):
    """
    Retrieve the top-k most relevant chunks for a user question.

    Parameters
    ----------
    query : str
        User's question.

    embedder : SentenceTransformer
        Embedding model.

    index : faiss.Index
        FAISS vector index.

    chunks : list[str]
        All text chunks.

    sources : list[str]
        Source URL for each chunk.

    k : int
        Number of chunks to retrieve.

    Returns
    -------
    list[dict]
        Retrieved chunk information.
    """


    if not chunks:
        return []

    query_embedding = embedder.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    k = min(k, len(chunks))

    distances, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        results.append({
            "text": chunks[idx],
            "source": sources[idx],
            "score": float(np.exp(-distance))
        })

    return results



# ------------------------------------------
# Generate Answer
# ------------------------------------------


def answer_question(question, context_hits, generator):
    """
    Generate an answer using the retrieved context.

    Parameters
    ----------
    question : str
        User's question.

    context_hits : list
        Retrieved chunks.

    generator :
        HuggingFace text-generation pipeline.

    Returns
    -------
    str
        Generated answer.
    """

    if not context_hits:
        context = "No relevant information found."    

    else:

        context_parts = []

        for hit in context_hits:

            context_parts.append(

                f"Source: {hit['source']}\n"

                f"Content: {hit['text']}"

            )

        context = "\n\n".join(context_parts)

    prompt = (

        "You are a helpful assistant.\n"

        "Answer the question using ONLY the provided context.\n"

        "If the answer is not in the context, say you don't know.\n\n"

        f"Context:\n{context}\n\n"

        f"Question: {question}\n\n"

        "Answer:"
    )

    response = generator(

        prompt,

        max_new_tokens=200,

        temperature=0.3,

        do_sample=True,

        truncation=True

    )

    generated_text = response[0]["generated_text"]

    answer = generated_text[len(prompt):].strip()

    return answer

# ------------------------------------------
# Main Function
# ------------------------------------------


def main():

    print("=" * 60)
    print("          Web RAG Chatbot")
    print("=" * 60)

    
    # -------------------------
    # Get URLs
    # -------------------------
  
   
    urls = []

    while True:

        try:

            n = int( input("How many URLs do you want to use? "))

            if n < 1:

                print("Please enter at least 1  valid URL.")
                continue

            break

        except ValueError:

            print("Please enter a valid number.")

    for i in range(n):

        while True:

            url = input(f"Enter URL {i+1}: " ).strip()

            if (
                url.startswith("http://")
                or
                url.startswith("https://")
            ):

                urls.append(url)
                break

            print("Invalid URL.")

    
    # Build the whole pipeline only once

    pipe = build_pipeline(urls)

    chunks = pipe["chunks"]
    sources = pipe["sources"]
    embedder = pipe["embedder"]
    index = pipe["index"]
    generator = pipe["generator"]


    # -------------------------
    # Chat Loop
    # -------------------------

    while True:

        question = input(
            "\nAsk a question (or type 'exit'): "
        ).strip()
    
        if question.lower() == "exit":

            break

        hits = retrieve(
            question,
            embedder,
            index,
            chunks,
            sources,
            k=3
             
        )

        print("\nEvidence\n")

        for i, hit in enumerate(hits, start=1):

            print("-" * 60)

            print(f"\nChunk {i}")

            print(f"Source : {hit['source']}")

            print(f"Score  : {hit['score']:.4f}")

            print()

            print(hit["text"][:400])

          

        answer = answer_question(

            question,

            hits,

            generator
        )

        print("\nAnswer\n")

        print(answer)

if __name__ == "__main__":

    main()