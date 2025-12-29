"""Bu dosya, projenin "Anayasası"dır.
Hangi sınıfın ne iş yapacağını belirler ama nasıl yapacağına karışmaz."""
from abc import ABC, abstractmethod

# --- Data Interfaces ---
class IDataManager(ABC):
    """Veri erişim katmanı için sözleşme."""
    @abstractmethod
    def get_languages(self) -> list: pass

    @abstractmethod
    def load_pair(self, lang1: str, lang2: str) -> bool: pass

    @abstractmethod
    def get_words(self) -> tuple: pass

# --- Game Logic Interfaces ---
class IScoreManager(ABC):
    """Skorlama mantığı."""
    @abstractmethod
    def add_points(self, amount: int): pass
    @abstractmethod
    def reset(self): pass
    @abstractmethod
    def get_current_score(self) -> int: pass

class IQuestionGenerator(ABC):
    """Soru üretme mantığı."""
    @abstractmethod
    def set_data(self, questions: list, answers: list): pass
    @abstractmethod
    def generate(self) -> dict: pass