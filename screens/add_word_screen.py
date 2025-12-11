import tkinter as tk
from tkinter import messagebox
import pandas
from constants import *
import os

class AddWordScreen(tk.Frame):
    """Yeni kelime çifti ekleme ekranı."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        label_info = tk.Label(self, text="Table.csv'ye eklenecek kelime çifti:",
                              font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG, wraplength=300)
        label_info.pack(side="top", fill="x", pady=(20, 10))

        # --- 1. Kelime (İngilizce) ---
        lbl_1 = tk.Label(self, text="English (Sütun 1):", font=("Arial", 10), bg=COLOR_BG)
        lbl_1.pack(pady=(5,0))
        self.entry_col1 = tk.Entry(self, width=20, font=FONT_NY_BOLD)
        self.entry_col1.pack(pady=5)

        # --- 2. Kelime (Türkçe) ---
        lbl_2 = tk.Label(self, text="Turkish (Sütun 2):", font=("Arial", 10), bg=COLOR_BG)
        lbl_2.pack(pady=(5,0))
        self.entry_col2 = tk.Entry(self, width=20, font=FONT_NY_BOLD)
        self.entry_col2.pack(pady=5)

        save_btn = tk.Button(self, text="Table.csv'ye Kaydet", font=FONT_NY_BOLD,
                             command=self.add_word_to_table,
                             fg=COLOR_BTN_FG, bg=COLOR_BTN_SAVE, width=20, height=1)
        save_btn.pack(pady=20)

        back_btn = tk.Button(self, width=10, height=1, text="Geri",
                             command=lambda: controller.show_frame("MenuScreen"),
                             bg=COLOR_BTN_BACK, fg="white")
        back_btn.pack(side="bottom", pady=20)

    def on_show(self):
        self.entry_col1.delete(0, "end")
        self.entry_col2.delete(0, "end")
        self.entry_col1.focus()

    def add_word_to_table(self):
        """Girilen çifti table.csv dosyasına kaydeder."""
        val1 = self.entry_col1.get().strip()
        val2 = self.entry_col2.get().strip()

        if not val1 or not val2:
            messagebox.showwarning("Eksik Bilgi", "Lütfen her iki kelimeyi de giriniz.")
            return

        # Hedef dosya: table.csv
        target_file = "table.csv"

        try:
            if os.path.exists(target_file):
                existing_data = pandas.read_csv(target_file)
            else:
                # Dosya yoksa varsayılan sütunlarla oluştur
                existing_data = pandas.DataFrame(columns=["English", "Turkish", "Spanish", "French", "Italian", "German"])
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya okunamadı: {e}")
            return

        # Sütun isimlerini belirle (Dosyadaki ilk iki sütunu baz alıyoruz)
        first_col = existing_data.columns[0]
        second_col = existing_data.columns[1]

        # Kelime kontrolü
        if not existing_data.empty and val1.lower() in existing_data[first_col].astype(str).str.lower().values:
            messagebox.showinfo("Bilgi", f"'{val1}' zaten listede mevcut.")
        else:
            # Yeni satır oluştur
            new_row = pandas.DataFrame({first_col: [val1], second_col: [val2]})
            # Concat ile ekle
            data = pandas.concat([existing_data, new_row], ignore_index=True)
            # Dosyaya yaz
            data.to_csv(target_file, index=False)

            messagebox.showinfo("Başarılı", f"Table.csv güncellendi:\n{val1} - {val2}")

            # Hafızadaki veriyi güncellemek için controller'daki veriyi sıfırla
            self.controller.current_data = None

            self.entry_col1.delete(0, "end")
            self.entry_col2.delete(0, "end")
            self.entry_col1.focus()