import tkinter as tk
from tkinter import messagebox
import pandas


from screens import (WelcomeScreen, MenuScreen, AddWordScreen,
                     LanguageSelectScreen, ModeSelectScreen)
from game_screens import MultipleChoiceScreen, WordMatchingScreen


from constants import COLOR_BG

class WordGameApp(tk.Tk):
    """
    Ana uygulama sınıfı. Tkinter'ın ana penceresidir .
    Tüm frameleri yönetir ve skoru tutar.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("KELİME OYUNU")
        self.config(padx=50, pady=50, bg=COLOR_BG)
        self.minsize(500, 600) # Biraz genişlettim

        # --- Oyunun Genel Durumu ---
        self.score = 0
        self.language_file = "table.csv"
        self.language_pair = ("English", "Turkish") # (Sütun1, Sütun2)
        self.words_file = "words.csv"

        # --- Ekran Yönetimi ---
        container = tk.Frame(self, bg=COLOR_BG)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Tüm ekran sınıflarını bir döngü ile oluştur
        # String anahtarlar kullanmak, show_frame metodunu daha basit hale getirir
        for F in (WelcomeScreen, MenuScreen, AddWordScreen, LanguageSelectScreen,
                  ModeSelectScreen, MultipleChoiceScreen, WordMatchingScreen):
            frame_name = F.__name__ # Sınıfın adını (örn: "WelcomeScreen") alır
            frame = F(container, self) # 'self' (yani WordGameApp) kontrolcü olarak gönderilir
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame("WelcomeScreen")

    def show_frame(self, frame_name):
        """Belirtilen sınıf adına sahip Frame'i (ekranı) öne getirir."""
        frame = self.frames[frame_name]


        if hasattr(frame, 'on_show'):
            frame.on_show()

        frame.tkraise()

    def set_language_file(self, file_name, lang_pair):
        """Kullanıcının seçtiği dil dosyasını ve sütun çiftini ayarlar."""
        self.language_file = file_name
        self.language_pair = lang_pair
        print(f"Dil ayarlandı: {file_name} ile {lang_pair} sütunları")
        self.show_frame("ModeSelectScreen")

    def get_data(self):
        """Seçili dil dosyasından veriyi okur."""
        try:
            data = pandas.read_csv(self.language_file)
            if data.empty:
                messagebox.showerror("Hata", f"{self.language_file} dosyası boş!")
                self.show_frame("MenuScreen")
                return None
            return data
        except FileNotFoundError:
            messagebox.showerror("Hata", f"{self.language_file} dosyası bulunamadı!")
            self.show_frame("MenuScreen")
            return None
        except pandas.errors.EmptyDataError:
            messagebox.showerror("Hata", f"{self.language_file} dosyası boş!")
            self.show_frame("MenuScreen")
            return None
        except Exception as e:
            messagebox.showerror("Hata", f"Beklenmedik bir hata oluştu: {e}")
            self.show_frame("MenuScreen")
            return None



if __name__ == "__main__":
    app = WordGameApp()
    app.mainloop()