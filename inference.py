from ngram_model import NgramModel
import pickle
import re


def clean_text(text):
    """Clean the input text similar to how training data was cleaned"""
    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace
    text = " ".join(text.split())
    return text


def load_model(model_path="email_ngram_model.pkl"):
    """Load the trained n-gram model"""
    try:
        with open(model_path, "rb") as f:
            ngrams = pickle.load(f)
        model = NgramModel()
        model.ngrams = ngrams
        print("Model loaded successfully!")
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise


def get_suggestions(model, text, num_suggestions=5):
    """Get word suggestions for the given text"""
    # Clean the input text
    cleaned_text = clean_text(text)

    # Convert input to lowercase and split into words
    words = cleaned_text.split()

    # Need at least n-1 words for prediction
    if len(words) < model.n - 1:
        return f"Please enter at least {model.n - 1} words"

    # Get the context (last n-1 words)
    context = tuple(words[-(model.n - 1) :])

    try:
        # Get suggestions
        suggestions = model.get_suggestions(context, num_suggestions)
        return suggestions
    except KeyError:
        return f"No suggestions found for context: {' '.join(context)}"


def main():
    # Load the model
    model = load_model()

    print("\nEmail completion assistant ready!")
    print("Enter 'q' to quit")
    print("Enter 'num X' to change number of suggestions (e.g., 'num 10')")
    print("Enter 'debug' to see cleaned input")
    print("Otherwise, type some words to get suggestions\n")

    num_suggestions = 5
    debug_mode = False

    while True:
        text = input("\nEnter text: ").strip()

        if text.lower() == "q":
            break

        if text.lower() == "debug":
            debug_mode = not debug_mode
            print(f"Debug mode: {'on' if debug_mode else 'off'}")
            continue

        if text.lower().startswith("num "):
            try:
                num_suggestions = int(text.split()[1])
                print(f"Number of suggestions set to {num_suggestions}")
                continue
            except:
                print("Invalid number format")
                continue

        if debug_mode:
            cleaned = clean_text(text)
            print(f"\nOriginal text: {text}")
            print(f"Cleaned text: {cleaned}")
            words = cleaned.split()
            if len(words) >= model.n - 1:
                context = tuple(words[-(model.n - 1) :])
                print(f"Context used: {context}")

        suggestions = get_suggestions(model, text, num_suggestions)
        print(f"\nSuggestions: {suggestions}")


if __name__ == "__main__":
    main()
