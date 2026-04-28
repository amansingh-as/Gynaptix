import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .faq_data import faq_data

class FAQBot:
    def __init__(self):
        self.questions = [q for q, a in faq_data]
        self.answers = [a for q, a in faq_data]

        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(self.questions)

    def get_response(self, user_query):
        user_vec = self.vectorizer.transform([user_query])
        similarity = cosine_similarity(user_vec, self.X)

        idx = np.argmax(similarity)

        if similarity[0][idx] < 0.3:
            return "Sorry, I couldn't understand. Please consult a doctor."

        return self.answers[idx]