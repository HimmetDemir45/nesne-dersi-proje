import tkinter as tk
from constants import *

class MenuScreen(tk.Frame):
    """Ana Menü Ekranı."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        menu_label = tk.Label(self, text="Ana Menü", font=FONT_COURIER_BOLD,
                              fg=COLOR_FG, bg=COLOR_BG, width=30, height=1)
        menu_label.pack(side="top", fill="x", pady=(2, 70))

        add_word_button = tk.Button(self, text="Kendi kelimelerini ekle", font=FONT_NY_BOLD,
                                    fg=COLOR_BTN_FG, bg=COLOR_BTN_ADD, width=30, height=3,
                                    command=lambda: controller.show_frame("AddWordScreen"))
        add_word_button.pack(side="top", pady=10, fill="x")

        play_button = tk.Button(self, text="Oyuna başla", font=FONT_NY_BOLD,
                                fg=COLOR_BTN_FG, bg=COLOR_BTN_PLAY, width=30, height=3,
                                command=lambda: controller.show_frame("LanguageSelectScreen"))
        play_button.pack(side="top", pady=10, fill="x")

        quit_game_button = tk.Button(self, text="Çıkış", command=controller.quit,
                                     fg=COLOR_BTN_FG, bg=COLOR_BTN_QUIT, width=10, height=2)
        quit_game_button.pack(side="bottom", pady=10)