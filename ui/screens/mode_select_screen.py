import tkinter as tk
from ui.abstract_screen import AbstractScreen
from core.game_features import MultipleChoiceGenerator, MatchGenerator

class ModeSelectScreen(AbstractScreen):
    def create_widgets(self):
        # --- Orta Alan ---
        center_frame = tk.Frame(self, bg="#F0F3F4")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="OYUN MODU SEÇİNİZ", font=("Helvetica", 20, "bold"),
                 bg="#F0F3F4").pack(pady=(0, 40))

        # Çoktan Seçmeli Butonu
        tk.Button(center_frame, text="ÇOKTAN SEÇMELİ", font=("Arial", 14, "bold"),
                  bg="#3498DB", fg="white", width=25, height=2,
                  command=self.start_multiple_choice).pack(pady=10)

        # Eşleştirme Butonu
        tk.Button(center_frame, text="EŞLEŞTİRME", font=("Arial", 14, "bold"),
                  bg="#9B59B6", fg="white", width=25, height=2,
                  command=self.start_matching).pack(pady=10)

        # --- Alt Alan ---
        tk.Button(self, text="Geri", command=lambda: self.navigate("LanguageSelectScreen"),
                  bg="#95A5A6", fg="white", width=15).pack(side="bottom", pady=30)

    def start_multiple_choice(self):
        gen = MultipleChoiceGenerator()
        self.controller.set_generator(gen)
        self.navigate("GameScreen")

    def start_matching(self):
        gen = MatchGenerator()
        self.controller.set_generator(gen)
        self.navigate("MatchScreen")
