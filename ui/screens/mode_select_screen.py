import tkinter as tk
from ui.abstract_screen import AbstractScreen
from core.game_features import MultipleChoiceGenerator, MatchGenerator

class ModeSelectScreen(AbstractScreen):
    def create_widgets(self):
        tk.Label(self, text="OYUN MODU SEÇİNİZ", font=("Helvetica", 20, "bold"),
                 bg="#F0F3F4").pack(pady=(100, 30))

        # Çoktan Seçmeli Butonu
        tk.Button(self, text="ÇOKTAN SEÇMELİ", font=("Arial", 14, "bold"),
                  bg="#3498DB", fg="white", width=25, height=2,
                  command=self.start_multiple_choice).pack(pady=15)

        # Eşleştirme Butonu
        tk.Button(self, text="EŞLEŞTİRME", font=("Arial", 14, "bold"),
                  bg="#9B59B6", fg="white", width=25, height=2,
                  command=self.start_matching).pack(pady=15)

        # Geri Butonu
        tk.Button(self, text="Geri", command=lambda: self.navigate("LanguageSelectScreen"),
                  bg="#95A5A6", fg="white", width=15).pack(side="bottom", pady=20)

    def start_multiple_choice(self):
        # 1. Stratejiyi Belirle (Generator'ı yükle)
        gen = MultipleChoiceGenerator()
        self.controller.set_generator(gen)

        # 2. Ekrana Git
        self.navigate("GameScreen")

    def start_matching(self):
        # 1. Stratejiyi Belirle
        gen = MatchGenerator()
        self.controller.set_generator(gen)

        # 2. Ekrana Git (Henüz bu ekranı yapmadık ama altyapısı hazır)
        # self.navigate("MatchScreen")
        print("Eşleştirme ekranı yakında...")