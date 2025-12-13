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

        tk.Button(self, width=15, height=2, text="Geri",
                  command=lambda: controller.show_frame("LanguageSelectScreen"),
                  bg=COLOR_BTN_BACK, fg="white").pack(side="bottom")

        tk.Button(self, text="Eşleştirme", fg="#333333", bg="#2196F3", width=60, height=3,
                  command=lambda: controller.show_frame("WordMatchingScreen")
                  ).pack(side="top", pady=(160,20))

        tk.Button(self, text="Çoktan Seçmeli", fg="#333333", bg="#FF7043", width=60, height=3,
                  command=lambda: controller.show_frame("MultipleChoiceScreen")
                  ).pack(side="top")