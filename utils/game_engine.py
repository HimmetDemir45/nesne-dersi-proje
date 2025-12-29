import random

class GameEngine:
    """
    Sorumluluk: Oyun kuralları, puanlama, soru üretme ve durumu yönetme.
    """
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.score = 0
        self.total_questions = 10
        self.current_question_index = 0

        # Çoktan Seçmeli Verileri
        self.current_question = ""
        self.current_correct_answer = ""
        self.current_options = []

        # Eşleştirme Oyunu Verileri
        self.current_match_map = {} # {Sol: Sağ} eşleşmelerini tutar

        # Genel Veri Havuzu
        self.questions_list = []
        self.answers_list = []

    def start_new_game(self):
        """Oyunu sıfırlar ve veriyi yükler."""
        self.score = 0
        self.current_question_index = 0
        self.questions_list, self.answers_list = self.data_manager.get_words_list()

    # --- ÇOKTAN SEÇMELİ MODU (Mevcut) ---
    def generate_question(self):
        if not self.questions_list or self.current_question_index >= self.total_questions:
            return None

        idx = random.randint(0, len(self.questions_list) - 1)
        self.current_question = self.questions_list[idx]
        self.current_correct_answer = self.answers_list[idx]

        options = [self.current_correct_answer]
        while len(options) < 4:
            wrong = random.choice(self.answers_list)
            if wrong != self.current_correct_answer and wrong not in options:
                options.append(wrong)

        random.shuffle(options)
        self.current_options = options
        self.current_question_index += 1

        return {
            "question": self.current_question,
            "options": self.current_options,
            "q_number": self.current_question_index,
            "total": self.total_questions
        }

    # --- EŞLEŞTİRME MODU (YENİ EKLENDİ) ---
    def generate_matches(self, count=4):
        """Eşleştirme ekranı için rastgele 4 çift üretir."""
        if not self.questions_list:
            return None

        # Elimizdeki kelime sayısı istenenden azsa hepsini al
        available_count = len(self.questions_list)
        safe_count = min(count, available_count)

        # Rastgele indeksler seç
        indices = random.sample(range(available_count), safe_count)

        self.current_match_map = {}
        left_side = []
        right_side = []

        for idx in indices:
            q = self.questions_list[idx]
            a = self.answers_list[idx]

            left_side.append(q)
            right_side.append(a)
            # Doğru eşleşmeyi hafızaya kaydet
            self.current_match_map[q] = a

        # Sağ tarafı karıştır (UI'ın yapmasına gerek yok, motor yapsın)
        random.shuffle(right_side)

        return {
            "left": left_side,
            "right": right_side
        }

    def check_match_pair(self, left_word, right_word):
        """Seçilen iki kelimenin eşleşip eşleşmediğini kontrol eder."""
        true_answer = self.current_match_map.get(left_word)
        is_correct = (true_answer == right_word)

        if is_correct:
            self.score += 5

        return is_correct, self.score

    def check_answer(self, selected_answer):
        """Çoktan seçmeli için kontrol."""
        is_correct = (selected_answer == self.current_correct_answer)
        if is_correct:
            self.score += 5
        return is_correct, self.score