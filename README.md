# Web Insight AI

Web Insight AI is a Retrieval-Augmented Generation (RAG) application that enables users to interact with website content using natural language. Users can provide one or more website URLs, and the application extracts the webpage content, processes it, and answers questions based on the retrieved information.

The project combines web scraping, semantic search, vector embeddings, and a Large Language Model (LLM) to provide accurate and context-aware responses. It demonstrates the practical implementation of a complete RAG pipeline using Python.

---

## Project Overview

Reading lengthy webpages to find specific information can be time-consuming. Web Insight AI simplifies this process by allowing users to ask questions directly about website content.

The application extracts text from webpages, divides it into smaller chunks, converts each chunk into vector embeddings using Sentence Transformers, stores them in a FAISS vector index, and retrieves the most relevant information when a question is asked. The retrieved context is then provided to the language model to generate an accurate response.

---

## Features

- Extracts content from one or multiple websites
- Processes webpage text into manageable chunks
- Generates vector embeddings using Sentence Transformers
- Stores embeddings using FAISS for efficient similarity search
- Retrieves the most relevant webpage content through semantic search
- Generates context-aware answers using Retrieval-Augmented Generation (RAG)
- Simple and interactive user interface built with Streamlit

---

## Technology Stack

**Programming Language**
- Python

**Libraries and Frameworks**
- Streamlit
- BeautifulSoup
- Requests
- Sentence Transformers
- FAISS
- Transformers
- NumPy

---

## Project Workflow

1. Enter one or more website URLs.
2. Extract webpage content using web scraping.
3. Clean and split the extracted text into smaller chunks.
4. Convert each chunk into vector embeddings using Sentence Transformers.
5. Store the embeddings in a FAISS vector database.
6. Enter a question related to the website content.
7. Retrieve the most relevant chunks using semantic search.
8. Generate the final answer using the retrieved context.

---

## Project Structure

```
Web Insight AI
│
├── .gitignore                             
├── README.md             
├── app.py                 # Streamlit application       
├── chunk.py               # Splits extracted text into chunks
├── index.py               # Creates and manages the FAISS index
├── ragchat.txt            # RAG pipeline and question answering
├── requirements.txt       # Project dependencies      
├── scraper.py             # Extracts content from webpages
└── style.css              # Custom UI styling
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/tamusyosus/web-rag-chat.git
```

Navigate to the project directory

```bash
cd web-rag-chat
```

Install the required packages

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## Future Improvements

- Support PDF documents
- Support additional document formats
- Maintain conversation history
- Integrate multiple LLMs
- Improve retrieval using reranking
- Deploy the application on the cloud

---

## Author

**Sushmita Gurung**
