from .interfaces import IDataManager, IScoreManager, IQuestionGenerator

class GameController:
    """
    Alt sistemlerin karmaşıklığını UI'dan saklar.
    Tüm bu parçaları (Veri, Skor, Üretici) yöneten beyin.
    """
    def __init__(self, data_manager: IDataManager, score_manager: IScoreManager):
        self.data_mgr = data_manager
        self.score_mgr = score_manager

        # O anki aktif soru üretici
        self.current_generator = None
        self.current_correct_answer = None
        self.current_match_pairs = {}

    def load_game_data(self, filename, l1, l2):
        return self.data_mgr.load_language_pair(filename, l1, l2)

    def set_generator(self, generator: IQuestionGenerator):
        """Hangi oyun oynanacaksa onun üreticisini yükle."""
        self.current_generator = generator
        q, a = self.data_mgr.get_words_list()
        self.current_generator.set_data(q, a)
        self.score_mgr.reset_score()

    # --- Çoktan Seçmeli Mantığı ---
    def next_question(self):
        if not self.current_generator: return None

        data = self.current_generator.generate()
        if data:
            self.current_correct_answer = data.get('correct')
        return data

    def check_choice(self, answer) -> bool:
        is_correct = (answer == self.current_correct_answer)
        if is_correct:
            self.score_mgr.add_points(5)
        return is_correct

    def add_new_word(self, filename, l1, v1, l2, v2):
        """Yeni kelime eklemek için DataManager'ı tetikler."""
        return self.data_mgr.add_word_pair(filename, l1, v1, l2, v2)

    def get_available_languages(self, filename):
        """Dil listesini DataManager'dan çeker."""
        return self.data_mgr.get_available_languages(filename)

    # --- Eşleştirme Mantığı ---
    def next_match_round(self):
        if not self.current_generator: return None
        data = self.current_generator.generate()
        if data:
            self.current_match_pairs = data.get('pairs')
        return data

    def check_match(self, left, right) -> bool:
        true_ans = self.current_match_pairs.get(left)
        is_correct = (true_ans == right)
        if is_correct:
            self.score_mgr.add_points(5)
        return is_correct

    def get_score(self):
        return self.score_mgr.get_score()