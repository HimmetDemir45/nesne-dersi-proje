import tkinter as tk
from tkinter import ttk  # Combobox için gerekli
from tkinter import messagebox
import pandas
import os
from constants import *

class AddWordScreen(tk.Frame):
    """
    Yeni kelime çifti ekleme ekranı (Dinamik Versiyon).
    Kullanıcı CSV'deki dilleri seçip o dillere ait kelime ekleyebilir.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        # --- Başlık ---
        label_info = tk.Label(self, text="Kelime Ekle",
                              font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        label_info.pack(side="top", fill="x", pady=(30, 20))

        # --- Dil Seçim ve Giriş Alanı Çerçevesi ---
        self.input_frame = tk.Frame(self, bg=COLOR_BG)
        self.input_frame.pack(pady=10)

        # Mevcut dilleri dosyadan çek
        self.available_languages = self.get_languages_from_csv("table.csv")
        if not self.available_languages:
            self.available_languages = ["English", "Turkish"]

        # --- 1. Dil Seçimi ve Kelime Girişi ---
        tk.Label(self.input_frame, text="1. Dil:", font=("Arial", 10, "bold"), bg=COLOR_BG).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.combo1 = ttk.Combobox(self.input_frame, values=self.available_languages, state="readonly", width=15)
        self.combo1.current(0)
        self.combo1.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="Kelime:", font=("Arial", 10), bg=COLOR_BG).grid(row=0, column=2, padx=5, pady=5)

        self.entry1 = tk.Entry(self.input_frame, width=20, font=FONT_NY_BOLD)
        self.entry1.grid(row=0, column=3, padx=5, pady=5)

        # --- 2. Dil Seçimi ve Kelime Girişi ---
        tk.Label(self.input_frame, text="2. Dil:", font=("Arial", 10, "bold"), bg=COLOR_BG).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.combo2 = ttk.Combobox(self.input_frame, values=self.available_languages, state="readonly", width=15)
        # Eğer birden fazla dil varsa ikincisini seç, yoksa birinciyi
        if len(self.available_languages) > 1:
            self.combo2.current(1)
        else:
            self.combo2.current(0)
        self.combo2.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="Kelime:", font=("Arial", 10), bg=COLOR_BG).grid(row=1, column=2, padx=5, pady=5)

        self.entry2 = tk.Entry(self.input_frame, width=20, font=FONT_NY_BOLD)
        self.entry2.grid(row=1, column=3, padx=5, pady=5)

        # --- Kaydet Butonu ---
        save_btn = tk.Button(self, text="KAYDET", font=FONT_NY_BOLD,
                             command=self.add_word_to_table,
                             fg=COLOR_BTN_FG, bg=COLOR_BTN_SAVE, width=20, height=2)
        save_btn.pack(pady=20)

        # --- Geri Butonu ---
        back_btn = tk.Button(self, width=15, height=1, text="Geri",
                             command=lambda: controller.show_frame("MenuScreen"),
                             bg=COLOR_BTN_BACK, fg="white")
        back_btn.pack(side="bottom", pady=20)

    def get_languages_from_csv(self, filename):
        """CSV dosyasının başlıklarını okur."""
        try:
            if not os.path.exists(filename):
                return []
            df = pandas.read_csv(filename, nrows=0) # Sadece başlığı oku
            return df.columns.tolist()
        except Exception as e:
            print(f"Dil listesi hatası: {e}")
            return []

    def on_show(self):
        """Ekran açıldığında dil listesini güncelle ve alanları temizle."""
        current_langs = self.get_languages_from_csv("table.csv")
        if current_langs:
            self.combo1['values'] = current_langs
            self.combo2['values'] = current_langs
            self.available_languages = current_langs

        self.entry1.delete(0, "end")
        self.entry2.delete(0, "end")
        self.entry1.focus()

    def add_word_to_table(self):
        """Seçilen dillere göre kelime çiftini kaydeder."""
        lang1 = self.combo1.get()
        lang2 = self.combo2.get()
        val1 = self.entry1.get().strip()
        val2 = self.entry2.get().strip()

        # 1. Kontrol: Diller ve Kelimeler Dolu mu?
        if not lang1 or not lang2:
            messagebox.showwarning("Hata", "Lütfen her iki dili de seçiniz.")
            return

        if not val1 or not val2:
            messagebox.showwarning("Eksik Bilgi", "Lütfen her iki kelimeyi de giriniz.")
            return

        target_file = "table.csv"

        try:
            # Dosyayı Oku
            if os.path.exists(target_file):
                # utf-8 encoding ekledik
                existing_data = pandas.read_csv(target_file, encoding='utf-8')
            else:
                # Dosya yoksa, seçilen dillerle yeni bir yapı oluştur
                columns = list(set(["English", "Turkish", lang1, lang2])) # Varsayılanlar + seçilenler
                existing_data = pandas.DataFrame(columns=columns)

            # 2. Kontrol: Kelime Zaten Var mı? (Sadece 1. dile göre basit kontrol)
            # Seçilen 1. dil dosya sütunlarında var mı diye bakıyoruz
            if lang1 in existing_data.columns:
                # Küçük harfe çevirip kontrol et
                if val1.lower() in existing_data[lang1].astype(str).str.lower().values:
                    messagebox.showinfo("Bilgi", f"'{val1}' kelimesi ({lang1}) zaten listede mevcut.")
                    return

            # --- Yeni Satırı Hazırla ---
            # Dosyadaki tüm sütunları boş string ile başlat
            new_row_data = {col: "" for col in existing_data.columns}

            # Seçilen dillere değerleri ata
            new_row_data[lang1] = val1
            new_row_data[lang2] = val2

            # DataFrame oluştur
            new_row = pandas.DataFrame([new_row_data])

            # Veriye Ekle (Concat)
            data = pandas.concat([existing_data, new_row], ignore_index=True)

            # Dosyayı Kaydet
            data.to_csv(target_file, index=False, encoding='utf-8')

            messagebox.showinfo("Başarılı", f"Kaydedildi:\n{lang1}: {val1}\n{lang2}: {val2}")

            # Hafızadaki veriyi sıfırla ki diğer ekranlar güncel veriyi çeksin
            self.controller.current_data = None

            # Alanları temizle
            self.entry1.delete(0, "end")
            self.entry2.delete(0, "end")
            self.entry1.focus()

        except Exception as e:
            messagebox.showerror("Hata", f"Dosya işlem hatası:\n{e}")