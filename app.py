import tkinter as tk
from tkinter import messagebox
from utils import DataManager, GameEngine
from screens import (WelcomeScreen, MenuScreen, AddWordScreen,
                     LanguageSelectScreen, ModeSelectScreen, ResultScreen)
from game_screens import MultipleChoiceScreen, WordMatchingScreen
from constants import COLOR_BG

class WordGameApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("KELİME OYUNU")
        self.config(padx=50, pady=50, bg=COLOR_BG)
        self.minsize(600, 700)

        # --- ÇEKİRDEK SINIFLARIN BAŞLATILMASI ---
        self.data_manager = DataManager()
        self.game_engine = GameEngine(self.data_manager)

        # Veri ve Oyun mantığı instance'ları oluşturuluyor
        container = tk.Frame(self, bg=COLOR_BG)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (WelcomeScreen, MenuScreen, AddWordScreen, LanguageSelectScreen,
                  ModeSelectScreen, MultipleChoiceScreen, WordMatchingScreen, ResultScreen):
            frame_name = F.__name__
            frame = F(container, self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomeScreen")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        if hasattr(frame, 'on_show'):
            frame.on_show()
        frame.tkraise()

    # --- ESKİ METOTLARIN YERİNİ ALAN KÖPRÜLER ---

    def set_language_config(self, filename, lang1, lang2):
        """LanguageSelectScreen artık burayı çağıracak."""
        success, message = self.data_manager.load_language_pair(filename, lang1, lang2)
        if success:
            print(f"Dil ayarlandı: {message}")
            self.show_frame("ModeSelectScreen")
        else:
            messagebox.showerror("Hata", message)

    # Not: load_data_into_memory ve get_data metotlarını tamamen SİLDİK.
    # Artık verilere self.data_manager üzerinden erişilecek.