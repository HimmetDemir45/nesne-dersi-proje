import tkinter as tk
from ui.abstract_screen import AbstractScreen

class MenuScreen(AbstractScreen):
    def create_widgets(self):

        center_frame = tk.Frame(self, bg="#F0F3F4")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="ANA MENÜ", font=("Helvetica", 20, "bold"),
                 bg="#F0F3F4").pack(side="top" ,pady=(0, 360))

        buttons = [
            ("Kelime Ekle", "AddWordScreen", "#3498DB"),
            ("Oyuna Başla", "LanguageSelectScreen", "#9B59B6"),
            ("Çıkış", None, "#E74C3C")
        ]

        for text, screen_name, color in buttons:
            cmd = (lambda s=screen_name: self.navigate(s)) if screen_name else self.quit_app
            tk.Button(center_frame, text=text, font=("Arial", 12, "bold"),
                      bg=color, fg="white", width=20, height=2,
                      command=cmd).pack(pady=8)

    def quit_app(self):
        self.manager.root.quit()