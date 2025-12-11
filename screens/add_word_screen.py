import tkinter as tk
from tkinter import messagebox
import pandas
from constants import *

class AddWordScreen(tk.Frame):
    """Yeni kelime çifti ekleme ekranı."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        # Başlık
        label_info = tk.Label(self, text="Eklemek istediğiniz kelime çiftini giriniz:",
                              font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG, wraplength=300)
        label_info.pack(side="top", fill="x", pady=(20, 10))

        # --- 1. Kelime (Örn: İngilizce) ---
        lbl_1 = tk.Label(self, text="Yabancı Dil (Örn: English):", font=("Arial", 10), bg=COLOR_BG)
        lbl_1.pack(pady=(5,0))
        self.entry_col1 = tk.Entry(self, width=20, font=FONT_NY_BOLD)
        self.entry_col1.pack(pady=5)

        # --- 2. Kelime (Örn: Türkçe) ---
        lbl_2 = tk.Label(self, text="Anadil (Örn: Türkçe):", font=("Arial", 10), bg=COLOR_BG)
        lbl_2.pack(pady=(5,0))
        self.entry_col2 = tk.Entry(self, width=20, font=FONT_NY_BOLD)
        self.entry_col2.pack(pady=5)

        # Kaydet Butonu
        save_btn = tk.Button(self, text="Kaydet", font=FONT_NY_BOLD,
                             command=self.add_word_to_csv,
                             fg=COLOR_BTN_FG, bg=COLOR_BTN_SAVE, width=15, height=1)
        save_btn.pack(pady=20)

        # Geri Butonu
        back_btn = tk.Button(self, width=10, height=1, text="Geri",
                             command=lambda: controller.show_frame("MenuScreen"),
                             bg=COLOR_BTN_BACK, fg="white")
        back_btn.pack(side="bottom", pady=20)

    def on_show(self):
        """Ekran açıldığında kutuları temizle ve odaklan."""
        self.entry_col1.delete(0, "end")
        self.entry_col2.delete(0, "end")
        self.entry_col1.focus()

    def add_word_to_csv(self):
        """Girilen çifti CSV'ye kaydeder."""
        val1 = self.entry_col1.get().strip()
        val2 = self.entry_col2.get().strip()

        if not val1 or not val2:
            messagebox.showwarning("Eksik Bilgi", "Lütfen her iki kelimeyi de giriniz.")
            return

        try:
            existing_data = pandas.read_csv(self.controller.words_file)
        except FileNotFoundError:
            existing_data = pandas.DataFrame(columns=["English", "Turkish"])

        # Sütun isimlerini dinamik veya varsayılan al
        if not existing_data.empty:
            first_col = existing_data.columns[0]
            second_col = existing_data.columns[1] if len(existing_data.columns) > 1 else "Turkish"
        else:
            first_col, second_col = "English", "Turkish"

        # Kelime var mı kontrolü
        if not existing_data.empty and val1.lower() in existing_data[first_col].str.lower().values:
            messagebox.showinfo("Bilgi", f"'{val1}' zaten listede mevcut.")
        else:
            new_row = pandas.DataFrame({first_col: [val1], second_col: [val2]})
            data = pandas.concat([existing_data, new_row], ignore_index=True)
            data.to_csv(self.controller.words_file, index=False)
            messagebox.showinfo("Başarılı", f"Eklendi: {val1} - {val2}")

            self.entry_col1.delete(0, "end")
            self.entry_col2.delete(0, "end")
            self.entry_col1.focus()