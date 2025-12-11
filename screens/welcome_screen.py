import tkinter as tk
from constants import COLOR_BG, COLOR_FG, FONT_COURIER_BOLD, FONT_COURIER_NORMAL

class WelcomeScreen(tk.Frame):
    """Giriş ekranı (Hoşgeldiniz)."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        welcome_label = tk.Label(self, text="Kelime oyunuma hoşgeldiniz",
                                 font=FONT_COURIER_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        welcome_label.pack(side="top", fill="x", pady=(2, 50))

        loading_label = tk.Label(self, text="Yükleniyor...", font=FONT_COURIER_NORMAL,
                                 fg=COLOR_FG, bg=COLOR_BG)
        loading_label.pack(side="top", fill="x")

        # 3 saniye sonra ana menüyü göster
        self.after(3000, lambda: controller.show_frame("MenuScreen"))