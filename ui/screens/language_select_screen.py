import tkinter as tk
from tkinter import ttk, messagebox
from ui.abstract_screen import AbstractScreen

class LanguageSelectScreen(AbstractScreen):
    def create_widgets(self):
        # --- Orta Alan (Başlık ve Seçimler) ---
        center_frame = tk.Frame(self, bg="#F0F3F4")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="Lütfen Dil Çiftini Seçiniz", font=("Helvetica", 18, "bold"),
                 bg="#F0F3F4").pack(pady=(0, 30))

        # Seçim Grid Alanı
        select_frame = tk.Frame(center_frame, bg="#F0F3F4")
        select_frame.pack(pady=10)

        # 1. Dil
        tk.Label(select_frame, text="Soru Dili:", font=("Arial", 12), bg="#F0F3F4").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.combo1 = ttk.Combobox(select_frame, state="readonly", width=15)
        self.combo1.grid(row=0, column=1, padx=10, pady=10)

        # 2. Dil
        tk.Label(select_frame, text="Cevap Dili:", font=("Arial", 12), bg="#F0F3F4").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.combo2 = ttk.Combobox(select_frame, state="readonly", width=15)
        self.combo2.grid(row=1, column=1, padx=10, pady=10)

        # Başlat Butonu
        tk.Button(center_frame, text="DEVAM ET", font=("Arial", 12, "bold"),
                  bg="#2ECC71", fg="white", width=20, height=2,
                  command=self.save_and_continue).pack(pady=30)

        # --- Alt Alan (Geri Butonu) ---
        # Geri butonunu ekranın en altına yapıştırıyoruz
        tk.Button(self, text="Geri Dön", command=lambda: self.navigate("MenuScreen"),
                  bg="#95A5A6", fg="white", width=15).pack(side="bottom", pady=30)

    def on_show(self):
        langs = self.controller.data_mgr.get_available_languages("table.csv")
        if not langs:
            langs = ["English", "Turkish"]

        self.combo1['values'] = langs
        self.combo2['values'] = langs

        if len(langs) >= 2:
            self.combo1.current(0)
            self.combo2.current(1)

    def save_and_continue(self):
        l1 = self.combo1.get()
        l2 = self.combo2.get()

        if l1 == l2:
            messagebox.showwarning("Hata", "Farklı diller seçmelisiniz!")
            return

        success, msg = self.controller.load_game_data("table.csv", l1, l2)

        if success:
            self.navigate("ModeSelectScreen")
        else:
            messagebox.showerror("Hata", msg)