import tkinter as tk
from constants import *

class LanguageSelectScreen(tk.Frame):
    """Dil seçme ekranı."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self, text="Lütfen dil seçiniz", font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG).pack(side="top", fill="x", pady=(20, 10))

        tk.Button(self, text="İngilizce - Türkçe", fg=COLOR_BTN_FG, bg=COLOR_BTN_EN_TR, height=2, width=30,
                  command=lambda: controller.set_language_file("table.csv", ("English", "Turkish"))
                  ).pack(pady=5)

        tk.Button(self, text="İngilizce - Fransızca", fg=COLOR_BTN_FG, bg=COLOR_BTN_EN_FR, height=2, width=30,
                  command=lambda: controller.set_language_file("en_fr.csv", ("English", "French"))
                  ).pack(pady=5)

        tk.Button(self, text="İngilizce - Almanca", fg=COLOR_BTN_FG, bg=COLOR_BTN_EN_DE, height=2, width=30,
                  command=lambda: controller.set_language_file("en_de.csv", ("English", "German"))
                  ).pack(pady=5)

        # --- YENİ EKLENEN BUTON ---
        tk.Button(self, text="Kendi Kelimelerim", fg=COLOR_BTN_FG, bg="#8E44AD", height=2, width=30,
                  command=lambda: controller.set_language_file(controller.words_file, ("English", "Turkish"))
                  ).pack(pady=5)

        tk.Button(self, text="Geri", command=lambda: controller.show_frame("MenuScreen"),
                  bg=COLOR_BTN_BACK, fg="white", height=2, width=10
                  ).pack(side="bottom", pady=20)