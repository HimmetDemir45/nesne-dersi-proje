import tkinter as tk
from tkinter import ttk  # Combobox için gerekli
from tkinter import messagebox
import pandas
import os
from constants import *


class LanguageSelectScreen(tk.Frame):
    """
    Dil seçme ekranı (Dinamik Versiyon).
    Kullanıcı CSV dosyasındaki herhangi iki dili seçip eşleştirebilir.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        # --- Başlık ---
        tk.Label(self, text="Lütfen Dil Çiftini Seçiniz", font=FONT_NY_BOLD,
                 fg=COLOR_FG, bg=COLOR_BG).pack(side="top", fill="x", pady=(30, 20))

        # --- Dil Listesini Hazırla ---
        self.available_languages = self.get_languages_from_csv("table.csv")

        # Eğer dosya okunamazsa varsayılan bir liste koyalım
        if not self.available_languages:
            self.available_languages = ["English", "Turkish"]

        # --- Seçim Alanı Çerçevesi ---
        select_frame = tk.Frame(self, bg=COLOR_BG)
        select_frame.pack(pady=10)

        # 1. Dil Seçimi
        tk.Label(select_frame, text="1. Dil (Soru):", font=("Arial", 12), bg=COLOR_BG).grid(row=0, column=0, padx=10,
                                                                                            pady=5)
        self.combo1 = ttk.Combobox(select_frame, values=self.available_languages, state="readonly", width=15)
        self.combo1.current(0)  # İlk sıradakini seç
        self.combo1.grid(row=0, column=1, padx=10, pady=5)

        # 2. Dil Seçimi
        tk.Label(select_frame, text="2. Dil (Cevap):", font=("Arial", 12), bg=COLOR_BG).grid(row=1, column=0, padx=10,
                                                                                             pady=5)
        self.combo2 = ttk.Combobox(select_frame, values=self.available_languages, state="readonly", width=15)

        # İkinci dili, eğer varsa listedeki ikinci eleman yap, yoksa birinciyi seç
        if len(self.available_languages) > 1:
            self.combo2.current(1)
        else:
            self.combo2.current(0)
        self.combo2.grid(row=1, column=1, padx=10, pady=5)

        # --- Oyunu Başlat Butonu ---
        tk.Button(self, text="SEÇİLEN DİLLERLE BAŞLA", fg=COLOR_BTN_FG, bg=COLOR_BTN_PLAY,
                  font=FONT_NY_BOLD, height=2, width=25,
                  command=self.start_custom_game
                  ).pack(pady=30)

        # --- Geri Butonu ---
        tk.Button(self, text="Geri", command=lambda: controller.show_frame("MenuScreen"),
                  bg=COLOR_BTN_BACK, fg="white", height=2, width=10
                  ).pack(side="bottom", pady=20)

    def get_languages_from_csv(self, filename):
        """CSV dosyasının sadece başlıklarını okuyarak dil listesini döndürür."""
        try:
            if not os.path.exists(filename):
                return []
            # Sadece ilk satırı (header) okuyoruz, performans için
            df = pandas.read_csv(filename, nrows=0)
            return df.columns.tolist()
        except Exception as e:
            print(f"Dil listesi alınırken hata: {e}")
            return []

    def start_custom_game(self):
        """Combobox'lardan seçilen dilleri alıp oyunu başlatır."""
        lang1 = self.combo1.get()
        lang2 = self.combo2.get()

        if not lang1 or not lang2:
            messagebox.showwarning("Hata", "Lütfen her iki dili de seçiniz.")
            return

        if lang1 == lang2:
            messagebox.showwarning("Hata", "Soru ve Cevap dili aynı olamaz! Lütfen farklı diller seçiniz.")
            return

        # Controller'a dosya ve seçilen sütunları gönder
        self.controller.set_language_file("table.csv", (lang1, lang2))

    def on_show(self):
        """
        Ekran her açıldığında (belki table.csv güncellenmiştir diye)
        listeyi yenilemek isteyebiliriz.
        """
        current_langs = self.get_languages_from_csv("table.csv")
        if current_langs:
            self.combo1['values'] = current_langs
            self.combo2['values'] = current_langs
            # Seçimleri koru veya sıfırla... Şimdilik olduğu gibi bırakıyoruz.
