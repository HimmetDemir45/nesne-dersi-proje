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
        self.used_indices = set() # Sorulan soruları takip etmek için
        self.counter = 0          # Şu anki soru sayısı
        self.limit = 10           # Toplam soru limiti

    def set_data(self, questions: list, answers: list):
        self.q_list = questions
        self.a_list = answers
        # Her yeni oyun başladığında sayacı ve geçmişi sıfırla
        self.used_indices = set()
        self.counter = 0

    def generate(self) -> dict:
        # Liste boşsa veya limit dolduysa None döndür (Oyun biter)
        if not self.q_list or self.counter >= self.limit:
            return None

        # Daha önce sorulmamış rastgele bir index bul
        available_indices = [i for i in range(len(self.q_list)) if i not in self.used_indices]

        if not available_indices: # Eğer havuzdaki kelimeler bittiyse
            return None

        idx = random.choice(available_indices)
        self.used_indices.add(idx) # Bu soruyu kullanıldı olarak işaretle

        correct_answer = self.a_list[idx]
        question_text = self.q_list[idx]

        # Şık üretimi
        options = [correct_answer]
        while len(options) < 4:
            wrong = random.choice(self.a_list)
            if wrong != correct_answer and wrong not in options:
                options.append(wrong)

        random.shuffle(options)
        self.counter += 1

        return {
            "question": question_text,
            "correct": correct_answer, # Doğru cevabı UI bilsin diye buraya ekledik
            "options": options,
            "index": self.counter,
            "total": self.limit
        }

class MatchGenerator(IQuestionGenerator):
    """Eşleştirme oyunu için özel üretici (Limitli ve Takipli)."""
    def __init__(self):
        self.q_list = []
        self.a_list = []
        self.used_indices = set()
        self.counter = 0
        self.limit = 10 # 10 Tur Sınırı

    def set_data(self, questions: list, answers: list):
        self.q_list = questions
        self.a_list = answers
        self.used_indices = set()
        self.counter = 0

    def generate(self, count=4) -> dict:
        # Limit kontrolü
        if self.counter >= self.limit:
            return None

        # Kullanılmamış kelimeleri bul
        available_indices = [i for i in range(len(self.q_list)) if i not in self.used_indices]

        # Eğer yeterli kelime kalmadıysa oyunu bitir
        if len(available_indices) < count:
            return None

        # Rastgele seçim yap
        indices = random.sample(available_indices, count)

        # Seçilenleri 'kullanıldı' olarak işaretle
        for idx in indices:
            self.used_indices.add(idx)

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
        self.counter += 1

        return {
            "left": left,
            "right": right,
            "pairs": pairs,
            "round": self.counter,
            "total_rounds": self.limit
        }