import tkinter as tk
from ui.abstract_screen import AbstractScreen

class WelcomeScreen(AbstractScreen):
    def create_widgets(self):
        # Ortaya hizalama için boşluklar
        self.pack_propagate(False)

        tk.Label(self, text="KELİME OYUNUNA\nHOŞGELDİNİZ",
                 font=("Helvetica", 24, "bold"), bg="#F0F3F4").pack(pady=(150, 30))

        tk.Button(self, text="BAŞLA", font=("Arial", 14, "bold"),
                  bg="#2ECC71", fg="white", width=15, height=2,
                  command=lambda: self.navigate("MenuScreen")).pack(pady=20)