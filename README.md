# Web Insight AI

Web Insight AI is a Retrieval-Augmented Generation (RAG) application that allows users to ask questions about the content of one or more websites. Instead of manually reading long webpages, users can enter website URLs and receive AI-generated answers based on the extracted webpage content.

The application extracts text from webpages, divides it into smaller chunks, converts them into vector embeddings using Sentence Transformers, stores them in a FAISS vector database, and retrieves the most relevant information to generate accurate and context-aware responses.

---

## Features

- Chat with the content of one or more websites
- Extract and process webpage text automatically
- Split webpage content into manageable text chunks
- Generate vector embeddings using Sentence Transformers
- Perform semantic search using FAISS
- Generate context-aware answers using Retrieval-Augmented Generation (RAG)
- Interactive user interface built with Streamlit

---

## Technology Stack

- Python
- Streamlit
- BeautifulSoup
- Requests
- Sentence Transformers
- FAISS
- Transformers
- NumPy

---

## Project Workflow

1. The user enters one or more website URLs.
2. The application extracts text from the webpages.
3. The extracted text is cleaned and divided into smaller chunks.
4. Sentence Transformers convert each chunk into vector embeddings.
5. FAISS stores the embeddings for efficient similarity search.
6. The user asks a question about the website content.
7. The application retrieves the most relevant text chunks using semantic search.
8. The retrieved context is passed to the language model to generate the final answer.

---

## Project Structure

```
Web Insight AI
│
├── app.py
├── scraper.py
├── chunk.py
├── index.py
├── ragchat.py
├── style.css
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/tamusyosus/web-rag-chat.git
```

Move into the project directory:

```bash
cd web-rag-chat
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## Future Improvements

- Support PDF documents
- Support additional document formats
- Maintain conversation history
- Support multiple language models
- Improve response quality with reranking
- Deploy the application on the cloud

---

## Author

Sushmita Gurung
