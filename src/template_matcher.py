from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import os


class TemplateMatcher:
    """
    Faz o mapeamento de uma pergunta em linguagem natural para um template.
    """
    def __init__(self, template_path):
        # Garante que o caminho seja relativo ao projeto
        template_path = os.path.abspath(template_path)

        with open(template_path, "r") as f:
            self.templates = json.load(f)

        self.vectorizer = TfidfVectorizer()
        self.template_vectors = self.vectorizer.fit_transform(self.templates)

    def predict_template(self, question):
        """
        Retorna o template mais próximo da pergunta.
        """
        question_vector = self.vectorizer.transform([question])
        similarities = cosine_similarity(question_vector, self.template_vectors)
        idx = np.argmax(similarities)
        return self.templates[idx]


if __name__ == "__main__":
    matcher = TemplateMatcher("src/templates.json")
    question = "Is our average employee older than 35?"
    template = matcher.predict_template(question)
    print(f"Template mapeado: {template}")
