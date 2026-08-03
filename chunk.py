def chunk_words(text, chunk_size=300, overlap=50):

    if overlap >= chunk_size:

        raise ValueError("Overlap must be smaller.")

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


