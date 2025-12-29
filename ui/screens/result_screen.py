import tkinter as tk
from ui.abstract_screen import AbstractScreen

class ResultScreen(AbstractScreen):
    def create_widgets(self):
        tk.Label(self, text="OYUN BİTTİ!", font=("Courier", 28, "bold"),
                 fg="#E74C3C", bg="#F0F3F4").pack(pady=(100, 20))

        self.lbl_final_score = tk.Label(self, text="Toplam Skor: 0",
                                        font=("Arial", 20), fg="#2C3E50", bg="#F0F3F4")
        self.lbl_final_score.pack(pady=20)

        # Butonlar
        tk.Button(self, text="Tekrar Oyna", font=("Arial", 12, "bold"),
                  bg="#3498DB", fg="white", width=20, height=2,
                  command=self.play_again).pack(pady=10)

        tk.Button(self, text="Ana Menü", font=("Arial", 12, "bold"),
                  bg="#95A5A6", fg="white", width=20, height=2,
                  command=lambda: self.navigate("MenuScreen")).pack(pady=10)

    def on_show(self):
        # Skoru Controller'dan al
        score = self.controller.get_score()
        self.lbl_final_score.config(text=f"Toplam Skor: {score}")

    def play_again(self):
        # Mod seçimine geri dön
        self.navigate("ModeSelectScreen")