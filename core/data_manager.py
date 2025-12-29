import pandas as pd
import os
from .interfaces import IDataManager

class CSVDataManager(IDataManager):
    """
    IDataManager arayüzünü uygulayan somut sınıf.
    """
    def __init__(self):
        self.current_data = None
        self.language_pair = None

    # Arayüzdeki 'get_available_languages' ile AYNI İSİMDE olmalı
    def get_available_languages(self, filename: str) -> list:
        try:
            if not os.path.exists(filename):
                return []
            df = pd.read_csv(filename, nrows=0)
            return df.columns.tolist()
        except Exception as e:
            print(f"Hata: {e}")
            return []

    # Arayüzdeki 'load_language_pair' ile AYNI İSİMDE olmalı
    def load_language_pair(self, filename: str, lang1: str, lang2: str) -> tuple[bool, str]:
        try:
            data = pd.read_csv(filename, usecols=[lang1, lang2])
            data = data.dropna()

            if data.empty:
                return False, "Dosya boş veya veri yok."

            self.current_data = data
            self.language_pair = (lang1, lang2)
            return True, "Veri başarıyla yüklendi."
        except ValueError:
            return False, f"Sütunlar bulunamadı: {lang1}, {lang2}"
        except FileNotFoundError:
            return False, "Dosya bulunamadı."
        except Exception as e:
            return False, f"Hata: {e}"

    # Arayüzdeki 'get_words_list' ile AYNI İSİMDE olmalı
    def get_words_list(self) -> tuple[list, list]:
        if self.current_data is None:
            return [], []
        lang1, lang2 = self.language_pair
        return self.current_data[lang1].tolist(), self.current_data[lang2].tolist()

    # Arayüzdeki 'add_word_pair' ile AYNI İSİMDE olmalı
    def add_word_pair(self, filename: str, lang1: str, val1: str, lang2: str, val2: str) -> tuple[bool, str]:
        try:
            if os.path.exists(filename):
                df = pd.read_csv(filename, encoding='utf-8')
            else:
                columns = list(set(["English", "Turkish", lang1, lang2]))
                df = pd.DataFrame(columns=columns)

            if lang1 not in df.columns: df[lang1] = ""
            if lang2 not in df.columns: df[lang2] = ""

            existing = df[lang1].astype(str).str.lower().values
            if val1.lower() in existing:
                return False, f"'{val1}' zaten listede var."

            new_row = {col: "" for col in df.columns}
            new_row[lang1] = val1
            new_row[lang2] = val2

            # Pandas sürümüne göre concat kullanımı
            new_df = pd.DataFrame([new_row])
            df = pd.concat([df, new_df], ignore_index=True)

            df.to_csv(filename, index=False, encoding='utf-8')

            self.current_data = None
            return True, "Kelime eklendi."
        except Exception as e:
            return False, f"Kayıt hatası: {e}"