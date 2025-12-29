from abc import ABC, abstractmethod

# --- Veri Yönetimi Arayüzü ---
class IDataManager(ABC):
    """
    Veri kaynağı ne olursa olsun (CSV, SQL, Excel),
    bu metotları barındırmak zorundadır.
    """
    @abstractmethod
    def get_available_languages(self, filename: str) -> list:
        pass

    @abstractmethod
    def load_language_pair(self, filename: str, lang1: str, lang2: str) -> tuple[bool, str]:
        pass

    @abstractmethod
    def get_words_list(self) -> tuple[list, list]:
        pass

    @abstractmethod
    def add_word_pair(self, filename: str, lang1: str, val1: str, lang2: str, val2: str) -> tuple[bool, str]:
        pass

# --- Oyun Mantığı Arayüzleri ---
class IScoreManager(ABC):
    @abstractmethod
    def add_points(self, amount: int): pass

    @abstractmethod
    def reset_score(self): pass

    @abstractmethod
    def get_score(self) -> int: pass

class IQuestionGenerator(ABC):
    @abstractmethod
    def set_data(self, questions: list, answers: list): pass

    @abstractmethod
    def generate(self) -> dict: pass