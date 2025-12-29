import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from constants import *

class AddWordScreen(tk.Frame):
    """
    Yeni kelime ekleme ekranı.
    Artık dosya işlemlerini DataManager'a devreder.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        # --- Başlık ---
        label_info = tk.Label(self, text="Kelime Ekle",
                              font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        label_info.pack(side="top", fill="x", pady=(30, 20))

        # --- Giriş Alanı ---
        self.input_frame = tk.Frame(self, bg=COLOR_BG)
        self.input_frame.pack(pady=10)

        # Listeyi DataManager'dan alacağız
        self.available_languages = []

        # 1. Dil
        tk.Label(self.input_frame, text="1. Dil:", font=("Arial", 10, "bold"), bg=COLOR_BG).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo1 = ttk.Combobox(self.input_frame, state="readonly", width=15)
        self.combo1.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="Kelime:", font=("Arial", 10), bg=COLOR_BG).grid(row=0, column=2, padx=5, pady=5)
        self.entry1 = tk.Entry(self.input_frame, width=20, font=FONT_NY_BOLD)
        self.entry1.grid(row=0, column=3, padx=5, pady=5)

        # 2. Dil
        tk.Label(self.input_frame, text="2. Dil:", font=("Arial", 10, "bold"), bg=COLOR_BG).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo2 = ttk.Combobox(self.input_frame, state="readonly", width=15)
        self.combo2.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="Kelime:", font=("Arial", 10), bg=COLOR_BG).grid(row=1, column=2, padx=5, pady=5)
        self.entry2 = tk.Entry(self.input_frame, width=20, font=FONT_NY_BOLD)
        self.entry2.grid(row=1, column=3, padx=5, pady=5)

        # --- Butonlar ---
        save_btn = tk.Button(self, text="KAYDET", font=FONT_NY_BOLD,
                             command=self.save_word,
                             fg=COLOR_BTN_FG, bg=COLOR_BTN_SAVE, width=20, height=2)
        save_btn.pack(pady=20)

        back_btn = tk.Button(self, width=15, height=1, text="Geri",
                             command=lambda: controller.show_frame("MenuScreen"),
                             bg=COLOR_BTN_BACK, fg="white")
        back_btn.pack(side="bottom", pady=20)

    def on_show(self):
        """Ekran açıldığında dil listesini DataManager'dan çek."""
        # YENİ YAPI: Controller -> DataManager
        langs = self.controller.data_manager.get_available_languages("table.csv")

        if not langs:
            langs = ["English", "Turkish"]

        self.available_languages = langs
        self.combo1['values'] = langs
        self.combo2['values'] = langs

        # Varsayılan seçimler
        if langs: self.combo1.current(0)
        if len(langs) > 1: self.combo2.current(1)
        elif langs: self.combo2.current(0)

        self.entry1.delete(0, "end")
        self.entry2.delete(0, "end")
        self.entry1.focus()

    def save_word(self):
        """DataManager üzerinden kayıt yap."""
        lang1 = self.combo1.get()
        lang2 = self.combo2.get()
        val1 = self.entry1.get().strip()
        val2 = self.entry2.get().strip()

        if not lang1 or not lang2:
            messagebox.showwarning("Hata", "Lütfen dilleri seçiniz.")
            return
        if not val1 or not val2:
            messagebox.showwarning("Hata", "Lütfen kelimeleri giriniz.")
            return

        # YENİ YAPI: İş mantığı DataManager'da
        success, message = self.controller.data_manager.add_word_pair("table.csv", lang1, val1, lang2, val2)

        if success:
            messagebox.showinfo("Başarılı", f"{message}\n({val1} - {val2})")
            self.entry1.delete(0, "end")
            self.entry2.delete(0, "end")
            self.entry1.focus()
        else:
            messagebox.showwarning("Hata", message)