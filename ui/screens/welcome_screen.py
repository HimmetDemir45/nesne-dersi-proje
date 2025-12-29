import tkinter as tk
from ui.abstract_screen import AbstractScreen

class WelcomeScreen(AbstractScreen):
    def create_widgets(self):
        # Tüm içeriği tutacak ve ortalayacak bir kutu (Container)
        center_frame = tk.Frame(self, bg="#F0F3F4")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="KELİME OYUNUNA\nHOŞGELDİNİZ",
                 font=("Helvetica", 24, "bold"), bg="#F0F3F4").pack(pady=20)

        tk.Button(center_frame, text="BAŞLA", font=("Arial", 14, "bold"),
                  bg="#2ECC71", fg="white", width=15, height=2,
                  command=lambda: self.navigate("MenuScreen")).pack(pady=20)