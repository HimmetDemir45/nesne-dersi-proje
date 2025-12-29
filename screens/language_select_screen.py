import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from constants import *

class LanguageSelectScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        # --- Başlık ---
        tk.Label(self, text="Lütfen Dil Çiftini Seçiniz", font=FONT_NY_BOLD,
                 fg=COLOR_FG, bg=COLOR_BG).pack(side="top", fill="x", pady=(120, 20))

        # --- Dil Listesini Hazırla ---
        # ARTIK DOĞRUDAN DOSYA OKUMUYORUZ
        self.available_languages = self.controller.data_manager.get_available_languages("table.csv")

        if not self.available_languages:
            self.available_languages = ["English", "Turkish"]

        # --- Seçim Alanı ---
        select_frame = tk.Frame(self, bg=COLOR_BG)
        select_frame.pack(pady=10)

        # 1. Dil
        tk.Label(select_frame, text="1. Dil (Soru):", font=("Arial", 12), bg=COLOR_BG).grid(row=0, column=0, padx=10, pady=30)
        self.combo1 = ttk.Combobox(select_frame, values=self.available_languages, state="readonly", width=15)
        self.combo1.current(0)
        self.combo1.grid(row=0, column=1, padx=10, pady=5)

        # 2. Dil
        tk.Label(select_frame, text="2. Dil (Cevap):", font=("Arial", 12), bg=COLOR_BG).grid(row=1, column=0, padx=10, pady=20)
        self.combo2 = ttk.Combobox(select_frame, values=self.available_languages, state="readonly", width=15)

        if len(self.available_languages) > 1:
            self.combo2.current(1)
        else:
            self.combo2.current(0)
        self.combo2.grid(row=1, column=1, padx=10, pady=5)

        # --- Butonlar ---
        tk.Button(self, text="Geri", command=lambda: controller.show_frame("MenuScreen"),
                  bg=COLOR_BTN_BACK, fg="white", height=2, width=15).pack(side="bottom", pady=20)

        tk.Button(self, text="SEÇİLEN DİLLERLE BAŞLA", fg=COLOR_BTN_FG, bg=COLOR_BTN_PLAY,
                  font=FONT_NY_BOLD, height=2, width=25,
                  command=self.start_custom_game).pack(side="bottom", pady=30)

    def start_custom_game(self):
        lang1 = self.combo1.get()
        lang2 = self.combo2.get()

        if lang1 == lang2:
            messagebox.showwarning("Hata", "Soru ve Cevap dili aynı olamaz!")
            return

        # YENİ YAPI: Controller üzerindeki köprüyü kullanıyoruz
        self.controller.set_language_config("table.csv", lang1, lang2)

    def on_show(self):
        """Ekran açıldığında listeyi yenile."""
        current_langs = self.controller.data_manager.get_available_languages("table.csv")
        if current_langs:
            self.combo1['values'] = current_langs
            self.combo2['values'] = current_langs