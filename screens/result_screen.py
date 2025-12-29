import tkinter as tk
from constants import *

class ResultScreen(tk.Frame):
    """Oyun bittiğinde skoru gösteren ekran."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        # Başlık
        tk.Label(self, text="OYUN BİTTİ!", font=("Courier", 30, "bold"),
                 fg=COLOR_FG, bg=COLOR_BG).pack(pady=(100, 20))

        # Skor Göstergesi
        self.final_score_label = tk.Label(self, text="Toplam Skor: 0",
                                          font=("Arial", 20), fg=COLOR_BTN_PLAY, bg=COLOR_BG)
        self.final_score_label.pack(pady=20)

        # Butonlar
        tk.Button(self, text="Tekrar Oyna", font=FONT_NY_BOLD,
                  bg=COLOR_BTN_MATCH, fg=COLOR_BTN_FG, width=20, height=2,
                  command=self.play_again).pack(pady=10)

        tk.Button(self, text="Ana Menü", font=FONT_NY_BOLD,
                  bg=COLOR_BTN_BACK, fg="white", width=20, height=2,
                  command=self.go_menu).pack(pady=10)

    def on_show(self):
        """Ekran açıldığında güncel skoru GameEngine'den al."""
        # YENİ YAPI: Controller -> GameEngine -> get_score()
        score = self.controller.game_engine.get_score()
        self.final_score_label.config(text=f"Toplam Skor: {score}")

    def play_again(self):
        """Skoru sıfırla ve son oynanan moda geri dön."""
        # Skoru burada sıfırlamaya gerek yok, oyun ekranları on_show'da start_new_game() yapıyor zaten.
        self.controller.show_frame("ModeSelectScreen")

    def go_menu(self):
        self.controller.show_frame("MenuScreen")