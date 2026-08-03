"""
scraper.py

Purpose:
1. Fetch webpage HTML.
2. Remove unnecessary HTML tags.
3. Extract clean text.
4. Download text from multiple webpages.
"""

import requests
from bs4 import BeautifulSoup


def fetch_text(url):
    """
    Fetch and clean text from a single webpage.

    Parameters:
        url (str): Webpage URL.

    Returns:
        str: Extracted text.
    """

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary HTML elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "header",
            "footer",
            "aside",
            "noscript"
        ]):
            tag.decompose()

        # Extract visible text
        text = soup.get_text(separator=" ")

        # Remove extra spaces and newlines
        clean_text = " ".join(text.split())

        return clean_text

    except Exception as e:
        print(f"Error fetching: {url}")
        print(e)
        return ""


def load_webpages(urls):
    """
    Download text from multiple webpages.

    Parameters:
        urls (list[str])

    Returns:
        tuple:
            texts   -> list of webpage text
            sources -> list of corresponding URLs
    """

    texts = []
    sources = []

    for url in urls:

        print(f"Reading: {url}")

        text = fetch_text(url)

        if text.strip():

            texts.append(text)

            sources.append(url)

        else:

            print("No text extracted.")

    return texts, sources


