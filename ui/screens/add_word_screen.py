import tkinter as tk
from tkinter import ttk, messagebox
from ui.abstract_screen import AbstractScreen

class AddWordScreen(AbstractScreen):
    def create_widgets(self):
        tk.Label(self, text="KELİME EKLE", font=("Helvetica", 18, "bold"),
                 bg="#F0F3F4").pack(pady=(50, 20))

        form_frame = tk.Frame(self, bg="#F0F3F4")
        form_frame.pack(pady=10)

        # 1. Dil ve Kelime
        tk.Label(form_frame, text="1. Dil:", bg="#F0F3F4").grid(row=0, column=0, padx=5, pady=5)
        self.combo1 = ttk.Combobox(form_frame, width=10, state="readonly")
        self.combo1.grid(row=0, column=1, padx=5)

        self.entry1 = tk.Entry(form_frame, width=15)
        self.entry1.grid(row=0, column=2, padx=5)

        # 2. Dil ve Kelime
        tk.Label(form_frame, text="2. Dil:", bg="#F0F3F4").grid(row=1, column=0, padx=5, pady=5)
        self.combo2 = ttk.Combobox(form_frame, width=10, state="readonly")
        self.combo2.grid(row=1, column=1, padx=5)

        self.entry2 = tk.Entry(form_frame, width=15)
        self.entry2.grid(row=1, column=2, padx=5)

        # Kaydet Butonu
        tk.Button(self, text="KAYDET", command=self.save,
                  bg="#2ECC71", fg="white", width=20).pack(pady=20)

        # Geri
        tk.Button(self, text="Geri", command=lambda: self.navigate("MenuScreen"),
                  bg="#95A5A6", fg="white").pack(side="bottom", pady=20)

    def on_show(self):
        # Controller üzerinden dil listesini al
        langs = self.controller.get_available_languages("table.csv")
        if not langs: langs = ["English", "Turkish"]

        self.combo1['values'] = langs
        self.combo2['values'] = langs
        if len(langs) >= 2:
            self.combo1.current(0)
            self.combo2.current(1)

        self.entry1.delete(0, "end")
        self.entry2.delete(0, "end")

    def save(self):
        l1, l2 = self.combo1.get(), self.combo2.get()
        v1, v2 = self.entry1.get(), self.entry2.get()

        if not v1 or not v2:
            messagebox.showwarning("Eksik", "Lütfen kelimeleri giriniz.")
            return

        # Controller üzerinden kayıt
        success, msg = self.controller.add_new_word("table.csv", l1, v1, l2, v2)

        if success:
            messagebox.showinfo("Başarılı", msg)
            self.entry1.delete(0, "end")
            self.entry2.delete(0, "end")
        else:
            messagebox.showerror("Hata", msg)