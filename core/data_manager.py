"""Burada IDataManager arayüzünü kullanarak gerçek işi yapan sınıfı (CSV okuyucuyu) yazıyoruz."""
import pandas as pd
import os
from .interfaces import IDataManager

class CSVDataManager(IDataManager):
    """
    CSV dosyaları ile çalışan somut DataManager sınıfı.
    """
    def __init__(self):
        self.current_data = None
        self.language_pair = None

    def get_available_languages(self, filename: str) -> list:
        try:
            if not os.path.exists(filename):
                return []
            df = pd.read_csv(filename, nrows=0)
            return df.columns.tolist()
        except Exception as e:
            print(f"Hata: {e}")
            return []

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

    def get_words_list(self) -> tuple[list, list]:
        if self.current_data is None:
            return [], []
        lang1, lang2 = self.language_pair
        return self.current_data[lang1].tolist(), self.current_data[lang2].tolist()

    def add_word_pair(self, filename: str, lang1: str, val1: str, lang2: str, val2: str) -> tuple[bool, str]:
        try:
            if os.path.exists(filename):
                df = pd.read_csv(filename, encoding='utf-8')
            else:
                columns = list(set(["English", "Turkish", lang1, lang2]))
                df = pd.DataFrame(columns=columns)

            if lang1 not in df.columns: df[lang1] = ""
            if lang2 not in df.columns: df[lang2] = ""

            # Basit kontrol (büyük/küçük harf duyarsız)
            existing = df[lang1].astype(str).str.lower().values
            if val1.lower() in existing:
                return False, f"'{val1}' zaten listede var."

            new_row = {col: "" for col in df.columns}
            new_row[lang1] = val1
            new_row[lang2] = val2

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(filename, index=False, encoding='utf-8')

            self.current_data = None # Cache temizle
            return True, "Kelime eklendi."
        except Exception as e:
            return False, f"Kayıt hatası: {e}"