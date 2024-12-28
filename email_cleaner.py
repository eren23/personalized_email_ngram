import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup


# Download all required NLTK data
def download_nltk_data():
    """Download required NLTK data"""
    required_data = ["punkt", "averaged_perceptron_tagger", "maxent_ne_chunker", "words", "stopwords"]

    for item in required_data:
        try:
            nltk.data.find(f"tokenizers/{item}")
        except LookupError:
            print(f"Downloading {item}...")
            nltk.download(item, quiet=True)


# Download NLTK data at import time
download_nltk_data()


def clean_email(text):
    # Convert HTML to text if present
    if "<html" in text.lower():
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text(separator=" ")

    # Remove email signatures
    text = re.sub(r"--\s*\n.*", "", text, flags=re.DOTALL)

    # Remove forwarded message headers
    text = re.sub(r"From:.*?\n", "", text)
    text = re.sub(r"Sent:.*?\n", "", text)
    text = re.sub(r"To:.*?\n", "", text)
    text = re.sub(r"Subject:.*?\n", "", text)

    # Remove URLs
    text = re.sub(r"http\S+|www.\S+", "", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", "", text)

    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Convert to lowercase
    text = text.lower()

    # Remove extra whitespace
    text = " ".join(text.split())

    return text


def tokenize_text(text):
    # Simple word tokenization using split
    # This is more reliable than word_tokenize when NLTK data isn't properly loaded
    tokens = text.split()
    return tokens
