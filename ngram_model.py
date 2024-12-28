from collections import defaultdict
import pickle


class NgramModel:
    """N-gram language model for text prediction."""

    def __init__(self, n=3):
        self.n = n
        self.ngrams = defaultdict(lambda: defaultdict(int))

    def train(self, tokens):
        for i in range(len(tokens) - self.n + 1):
            context = tuple(tokens[i : i + self.n - 1])
            next_word = tokens[i + self.n - 1]
            self.ngrams[context][next_word] += 1

    def get_suggestions(self, context, num_suggestions=5):
        context = tuple(context) if isinstance(context, list) else context
        next_words = self.ngrams[context]
        suggestions = sorted(next_words.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in suggestions[:num_suggestions]]

    def save_model(self, filepath):
        with open(filepath, "wb") as f:
            pickle.dump(dict(self.ngrams), f)

    def load_model(self, filepath):
        with open(filepath, "rb") as f:
            self.ngrams = defaultdict(lambda: defaultdict(int), pickle.load(f))
