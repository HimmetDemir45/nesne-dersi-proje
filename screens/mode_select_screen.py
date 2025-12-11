import tkinter as tk
from constants import *

class ModeSelectScreen(tk.Frame):
    """Oyun modu seçme ekranı."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        choose_mode_label = tk.Label(self, text="Hangi modu oynamak istiyorsunuz?",
                                     font=FONT_COURIER_BOLD, fg=COLOR_FG, bg=COLOR_BG,
                                     width=33, height=2, wraplength=400)
        choose_mode_label.pack(side="top", pady=(2, 20))

        tk.Button(self, width=10, height=2, text="Geri",
                  command=lambda: controller.show_frame("LanguageSelectScreen"),
                  bg=COLOR_BTN_BACK, fg="white").pack(side="bottom")

        tk.Button(self, text="Eşleştirme", fg=COLOR_BTN_FG, bg=COLOR_BTN_MATCH, width=30, height=2,
                  command=lambda: controller.show_frame("WordMatchingScreen")
                  ).pack(side="bottom", pady=10)

        tk.Button(self, text="Çoktan Seçmeli", fg=COLOR_BTN_FG, bg=COLOR_BTN_CHOICE, width=30, height=2,
                  command=lambda: controller.show_frame("MultipleChoiceScreen")
                  ).pack(side="bottom", pady=10)