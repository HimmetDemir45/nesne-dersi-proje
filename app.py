import tkinter as tk
from tkinter import messagebox
import pandas

# Paketlerimizden sınıfları çekiyoruz
from screens import (WelcomeScreen, MenuScreen, AddWordScreen,
                     LanguageSelectScreen, ModeSelectScreen, ResultScreen)
from game_screens import MultipleChoiceScreen, WordMatchingScreen

from constants import COLOR_BG

class WordGameApp(tk.Tk):
    """
    Ana uygulama sınıfı.
    Tüm ekran geçişlerini ve veri yönetimini sağlar.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("KELİME OYUNU")
        self.config(padx=50, pady=50, bg=COLOR_BG)
        # Pencere boyutunu biraz genişlettik
        self.minsize(600, 700)

        # --- Oyun Verileri ---
        self.score = 0
        self.language_file = "table.csv"
        self.language_pair = ("English", "Turkish") # Varsayılan
        self.words_file = "words.csv"

        # Performans İyileştirmesi: Veriyi hafızada tut
        self.current_data = None

        # --- Ekran Yönetimi (Container) ---
        container = tk.Frame(self, bg=COLOR_BG)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Tüm ekran sınıflarını döngüyle oluşturup stack'e atıyoruz
        for F in (WelcomeScreen, MenuScreen, AddWordScreen, LanguageSelectScreen,
                  ModeSelectScreen, MultipleChoiceScreen, WordMatchingScreen, ResultScreen):
            frame_name = F.__name__
            # 'self' parametresi ile main uygulamanın kendisini (controller) gönderiyoruz
            frame = F(container, self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomeScreen")

    def show_frame(self, frame_name):
        """İstenilen ekranı en öne getirir."""
        frame = self.frames[frame_name]
        # Eğer ekranın kendine ait bir hazırlık metodu varsa (on_show) çalıştır
        if hasattr(frame, 'on_show'):
            frame.on_show()
        frame.tkraise()

    def set_language_file(self, file_name, lang_pair):
        """
        Kullanıcı bir dil seçtiğinde çalışır.
        Dosyayı okumayı dener, başarılıysa mod seçme ekranına geçer.
        """
        self.language_file = file_name
        self.language_pair = lang_pair

        # Veriyi hemen yüklemeyi dene
        if self.load_data_into_memory():
            print(f"Dil ayarlandı: {file_name} -> {lang_pair}")
            self.show_frame("ModeSelectScreen")

    def load_data_into_memory(self):
        """
        Seçili CSV dosyasını okur ve self.current_data değişkenine kaydeder.
        """
        try:
            data = pandas.read_csv(self.language_file)

            if data.empty:
                messagebox.showerror("Hata", f"{self.language_file} dosyası boş! Lütfen önce kelime ekleyin.")
                return False

            col1, col2 = self.language_pair

            # Eğer 'Kendi Kelimelerim' seçildiyse ve sütun isimleri farklıysa esneklik sağla
            if self.language_file == self.words_file:
                if len(data.columns) >= 2:
                    col1 = data.columns[0]
                    col2 = data.columns[1]
                    self.language_pair = (col1, col2)

            if col1 not in data.columns or col2 not in data.columns:
                messagebox.showerror("Hata", f"Dosyada gerekli sütunlar ({col1}, {col2}) bulunamadı.\nDosya Sütunları: {list(data.columns)}")
                return False

            self.current_data = data
            return True

        except FileNotFoundError:
            if self.language_file == self.words_file:
                messagebox.showerror("Hata", "Henüz kendi kelimelerinizi oluşturmadınız. 'Kelime Ekle' menüsünü kullanın.")
            else:
                messagebox.showerror("Hata", f"{self.language_file} dosyası bulunamadı!")
            return False
        except Exception as e:
            messagebox.showerror("Hata", f"Beklenmedik bir hata oluştu: {e}")
            return False

    def get_data(self):
        """Oyun ekranları veri istediğinde bu metodu çağırır."""
        if self.current_data is None:
            success = self.load_data_into_memory()
            if not success:
                return None
        return self.current_data