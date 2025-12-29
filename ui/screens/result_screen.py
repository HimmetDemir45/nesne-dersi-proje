import tkinter as tk
from ui.abstract_screen import AbstractScreen

class ResultScreen(AbstractScreen):
    def create_widgets(self):
        # Ortalamak için Container
        center_frame = tk.Frame(self, bg="#F0F3F4")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="OYUN BİTTİ!", font=("Courier", 28, "bold"),
                 fg="#E74C3C", bg="#F0F3F4").pack(pady=10)

        self.lbl_final_score = tk.Label(center_frame, text="Toplam Skor: 0",
                                        font=("Arial", 20), fg="#2C3E50", bg="#F0F3F4")
        self.lbl_final_score.pack(pady=30)

        # Butonlar
        tk.Button(center_frame, text="Tekrar Oyna", font=("Arial", 12, "bold"),
                  bg="#3498DB", fg="white", width=20, height=2,
                  command=self.play_again).pack(pady=10)

        tk.Button(center_frame, text="Ana Menü", font=("Arial", 12, "bold"),
                  bg="#95A5A6", fg="white", width=20, height=2,
                  command=lambda: self.navigate("MenuScreen")).pack(pady=10)

    def on_show(self):
        score = self.controller.get_score()
        self.lbl_final_score.config(text=f"Toplam Skor: {score}")

    def play_again(self):
        self.navigate("ModeSelectScreen")