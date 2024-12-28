"""Main script for training the email-based text prediction model."""

from email_downloader import connect_to_gmail, download_emails
from email_cleaner import clean_email, tokenize_text
from ngram_model import NgramModel
import os
from dotenv import load_dotenv
import subprocess
import sys


def install_requirements():
    """Install required packages if they're not already installed."""
    required_packages = ["beautifulsoup4", "nltk", "python-dotenv"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def main():
    """Main function to train and test the model."""
    install_requirements()
    load_dotenv()

    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")

    try:
        imap = connect_to_gmail(email_address, email_password)
        emails = download_emails(imap, max_emails=5000)
        imap.logout()
    except Exception as e:
        print(f"Error downloading emails: {str(e)}")
        raise

    all_tokens = []
    for email_text in emails:
        cleaned_text = clean_email(email_text)
        tokens = tokenize_text(cleaned_text)
        all_tokens.extend(tokens)

    model = NgramModel(n=3)
    model.train(all_tokens)
    model.save_model("email_ngram_model.pkl")

    while True:
        prompt = "Enter the beginning of your sentence (or 'q' to quit): "
        context = input(prompt).lower().split()
        if context[0] == "q":
            break

        if len(context) >= model.n - 1:
            context = tuple(context[-(model.n - 1) :])
            suggestions = model.get_suggestions(context)
            print("Suggestions:", suggestions)
        else:
            print("Please enter at least", model.n - 1, "words")


if __name__ == "__main__":
    main()
