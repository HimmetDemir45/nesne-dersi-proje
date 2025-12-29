"""Skor yönetimi ve soru üretme mantığını buraya alıyoruz. Tek bir büyük GameEngine yerine parçalara bölüyoruz."""
import random
from .interfaces import IScoreManager, IQuestionGenerator

class BasicScoreManager(IScoreManager):
    def __init__(self):
        self._score = 0

    def add_points(self, amount: int):
        self._score += amount

    def reset_score(self):
        self._score = 0

    def get_score(self) -> int:
        return self._score

class MultipleChoiceGenerator(IQuestionGenerator):
    def __init__(self):
        self.q_list = []
        self.a_list = []

    def set_data(self, questions: list, answers: list):
        self.q_list = questions
        self.a_list = answers

    def generate(self) -> dict:
        if not self.q_list:
            return None

        idx = random.randint(0, len(self.q_list) - 1)
        correct_answer = self.a_list[idx]
        question_text = self.q_list[idx]

        # Şık üretimi
        options = [correct_answer]
        while len(options) < 4:
            wrong = random.choice(self.a_list)
            if wrong != correct_answer and wrong not in options:
                options.append(wrong)

        random.shuffle(options)

        return {
            "question": question_text,
            "correct": correct_answer,
            "options": options,
            "index": idx + 1,
            "total": len(self.q_list) # Toplam soru sayısı yerine havuz boyutunu veriyoruz
        }

class MatchGenerator(IQuestionGenerator):
    """Eşleştirme oyunu için özel üretici."""
    def __init__(self):
        self.q_list = []
        self.a_list = []

    def set_data(self, questions: list, answers: list):
        self.q_list = questions
        self.a_list = answers

    def generate(self, count=4) -> dict:
        if not self.q_list: return None

        limit = min(count, len(self.q_list))
        indices = random.sample(range(len(self.q_list)), limit)

        pairs = {}
        left = []
        right = []

        for i in indices:
            q = self.q_list[i]
            a = self.a_list[i]
            left.append(q)
            right.append(a)
            pairs[q] = a

        random.shuffle(right)

        return {
            "left": left,
            "right": right,
            "pairs": pairs
        }