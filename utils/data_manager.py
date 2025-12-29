import pandas as pd
import os

class DataManager:
    """
    Veri okuma, yazma ve filtreleme işlerini yönetir.
    """
    def __init__(self):
        self.current_data = None
        self.language_pair = None

    def get_available_languages(self, filename="table.csv"):
        try:
            if not os.path.exists(filename):
                return []
            df = pd.read_csv(filename, nrows=0)
            return df.columns.tolist()
        except Exception as e:
            print(f"Hata: {e}")
            return []

    def load_language_pair(self, filename, lang1, lang2):
        try:
            data = pd.read_csv(filename, usecols=[lang1, lang2])
            data = data.dropna()

            if data.empty:
                return False, "Veri yok."

            self.current_data = data
            self.language_pair = (lang1, lang2)
            return True, "Yüklendi."
        except Exception as e:
            return False, f"Hata: {e}"

    def get_words_list(self):
        if self.current_data is None:
            return None, None
        lang1, lang2 = self.language_pair
        return self.current_data[lang1].tolist(), self.current_data[lang2].tolist()

    # --- YENİ EKLENEN METOT: KELİME EKLEME ---
    def add_word_pair(self, filename, lang1, val1, lang2, val2):
        """Yeni kelime çiftini CSV dosyasına ekler."""
        try:
            # Dosyayı Oku
            if os.path.exists(filename):
                df = pd.read_csv(filename, encoding='utf-8')
            else:
                # Dosya yoksa oluştur
                columns = list(set(["English", "Turkish", lang1, lang2]))
                df = pd.DataFrame(columns=columns)

            # Sütun Kontrolü: Eğer seçilen diller dosyada yoksa sütun ekle
            if lang1 not in df.columns: df[lang1] = ""
            if lang2 not in df.columns: df[lang2] = ""

            # Tekrar Kontrolü (Basitçe 1. dile bakıyoruz)
            # Küçük harfe çevirip kıyaslayalım
            existing_words = df[lang1].astype(str).str.lower().values
            if val1.lower() in existing_words:
                return False, f"'{val1}' kelimesi zaten mevcut."

            # Yeni satır oluştur
            new_row = {col: "" for col in df.columns}
            new_row[lang1] = val1
            new_row[lang2] = val2

            # DataFrame'e ekle (Concat kullanımı pandas'ın yeni sürümleri için daha uygundur)
            new_df = pd.DataFrame([new_row])
            df = pd.concat([df, new_df], ignore_index=True)

            # Kaydet
            df.to_csv(filename, index=False, encoding='utf-8')

            # Hafızayı tazele (Cache Invalidation)
            self.current_data = None

            return True, "Kelime başarıyla eklendi."

        except Exception as e:
            return False, f"Dosya hatası: {e}"