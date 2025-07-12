import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class TemplateMatcher:
    def __init__(self, template_path):
        with open(template_path, "r") as f:
            self.templates = json.load(f)

        self.vectorizer = TfidfVectorizer()
        self.template_vectors = self.vectorizer.fit_transform(self.templates)

    def predict_template(self, question):
        question_lower = question.lower()

        # Regras específicas primeiro
        if "highest" in question_lower and "rating" in question_lower and ("equal" in question_lower or "to" in question_lower):
            return "check if maximum equals value"

        if "bigger than" in question_lower or "more than" in question_lower:
            return "compare size of group A vs group B"

        if "highest average" in question_lower:
            return "calculate average of column"

        if "most common" in question_lower or "most frequent" in question_lower:
            return "get most common value of column"

        if "least common" in question_lower or "employ the least" in question_lower:
            return "get least common value of column"

        if "equal to" in question_lower:
            return "check if maximum equals value"

        if "negative" in question_lower:
            return "check if maximum is negative"

        if "are all" in question_lower or "same across" in question_lower:
            return "check if all values in column are equal"

        if "sum of" in question_lower:
            return "sum column"

        if "range of" in question_lower:
            return "calculate range of column"

        if "median of" in question_lower:
            return "calculate median of column"

        if "standard deviation" in question_lower:
            return "calculate std deviation of column"

        if "list" in question_lower or "show" in question_lower:
            return "list values in column"

        if "filter" in question_lower or "about" in question_lower:
            return "filter then get top-n"

        if "total number of different" in question_lower or "how many different" in question_lower:
            return "count distinct values of column"

        if "maximum years" in question_lower or "longest" in question_lower:
            return "get maximum of column"

        # fallback TF-IDF
        question_vector = self.vectorizer.transform([question])
        similarities = cosine_similarity(question_vector, self.template_vectors)
        idx = np.argmax(similarities)
        return self.templates[idx]
