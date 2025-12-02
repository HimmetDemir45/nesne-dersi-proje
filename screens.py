import tkinter as tk
from tkinter import messagebox
import pandas


from constants import *

class WelcomeScreen(tk.Frame):
    """Giriş ekranı (Hoşgeldiniz)."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        welcome_label = tk.Label(self, text="Kelime oyunuma hoşgeldiniz",
                                 font=FONT_COURIER_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        welcome_label.pack(side="top", fill="x", pady=(2, 50))

        loading_label = tk.Label(self, text="Yükleniyor...", font=FONT_COURIER_NORMAL,
                                 fg=COLOR_FG, bg=COLOR_BG)
        loading_label.pack(side="top", fill="x")

        # 3 saniye sonra ana menüyü göster
        self.after(3000, lambda: controller.show_frame("MenuScreen"))


class MenuScreen(tk.Frame):
    """Ana Menü Ekranı (Kelime Ekle, Oyuna Başla, Çıkış)."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        menu_label = tk.Label(self, text="Ana Menü", font=FONT_COURIER_BOLD,
                              fg=COLOR_FG, bg=COLOR_BG, width=30, height=1)
        menu_label.pack(side="top", fill="x", pady=(2, 70))

        add_word_button = tk.Button(self, text="Kendi kelimelerini ekle", font=FONT_NY_BOLD,
                                    fg=COLOR_BTN_FG, bg=COLOR_BTN_ADD, width=30, height=3,
                                    command=lambda: controller.show_frame("AddWordScreen"))
        add_word_button.pack(side="top", pady=10, fill="x")

        play_button = tk.Button(self, text="Oyuna başla", font=FONT_NY_BOLD,
                                fg=COLOR_BTN_FG, bg=COLOR_BTN_PLAY, width=30, height=3,
                                command=lambda: controller.show_frame("LanguageSelectScreen"))
        play_button.pack(side="top", pady=10, fill="x")

        quit_game_button = tk.Button(self, text="Çıkış", command=controller.quit,
                                     fg=COLOR_BTN_FG, bg=COLOR_BTN_QUIT, width=10, height=2)
        quit_game_button.pack(side="bottom", pady=10)


class AddWordScreen(tk.Frame):
    """Yeni kelime ekleme ekranı."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        add_word_label = tk.Label(self, text="Lütfen eklemek istediğiniz kelimeyi giriniz:",
                                  font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG, wraplength=300)
        add_word_label.pack(side="top", fill="x", pady=(2, 10))

        word_back_button = tk.Button(self, width=3, height=1, text="Geri",
                                     command=lambda: controller.show_frame("MenuScreen"),
                                     bg=COLOR_BTN_BACK, fg="white")
        word_back_button.pack(side="bottom", pady=10)

        add_word_button = tk.Button(self, text="Kaydet", font=FONT_NY_BOLD,
                                    command=self.add_word_to_csv,
                                    fg=COLOR_BTN_FG, bg=COLOR_BTN_SAVE, width=9, height=1)
        add_word_button.pack(side="bottom", pady=10)

        self.add_word_entry = tk.Entry(self, width=15, font=FONT_NY_BOLD)
        self.add_word_entry.pack(side="bottom", pady=10)
        self.add_word_entry.focus()

    def on_show(self):
        """Ekran gösterildiğinde focus'u ayarla."""
        self.add_word_entry.focus()

    def add_word_to_csv(self):
        """Entry'deki kelimeyi CSV dosyasına kaydeder."""
        word = self.add_word_entry.get().strip()
        if not word:
            messagebox.showwarning("Uyarı", "Lütfen bir kelime girin.")
            return

        try:
            existing_data = pandas.read_csv(self.controller.words_file)
        except FileNotFoundError:
            existing_data = pandas.DataFrame(columns=["English"])

        if word.lower() in existing_data["English"].str.lower().values:
            messagebox.showinfo("Bilgi", "Bu kelime zaten listede mevcut.")
        else:
            new_row = pandas.DataFrame({"English": [word]})
            data = pandas.concat([existing_data, new_row], ignore_index=True)
            data.to_csv(self.controller.words_file, index=False)
            messagebox.showinfo("Başarılı", f"'{word}' kelimesi eklendi.")

        self.add_word_entry.delete(0, "end")


class LanguageSelectScreen(tk.Frame):
    """Dil seçme ekranı."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        select_language_label = tk.Label(self, text="Lütfen dil seçiniz",
                                         font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        select_language_label.pack(side="top", fill="x", pady=(2, 10))

        tk.Button(self, text="EN/TR", fg=COLOR_BTN_FG, bg=COLOR_BTN_EN_TR, height=2, width=30,
                  command=lambda: controller.set_language_file("table.csv", ("English", "Turkish"))
                  ).pack(side="top", fill="x", pady=10)

        # Diğer diller için (dosya adları ve sütun adları örnek olarak verilmiştir)
        tk.Button(self, text="EN/FR", fg=COLOR_BTN_FG, bg=COLOR_BTN_EN_FR, height=2, width=30,
                  command=lambda: controller.set_language_file("en_fr.csv", ("English", "French"))
                  ).pack(side="top", fill="x", pady=10)

        tk.Button(self, text="EN/DE", fg=COLOR_BTN_FG, bg=COLOR_BTN_EN_DE, height=2, width=30,
                  command=lambda: controller.set_language_file("en_de.csv", ("English", "German"))
                  ).pack(side="top", fill="x", pady=10)

        # ... Diğer butonlar ...

        tk.Button(self, text="Geri", command=lambda: controller.show_frame("MenuScreen"),
                  bg=COLOR_BTN_BACK, fg="white", height=2, width=10
                  ).pack(side="bottom", pady=10)


class ModeSelectScreen(tk.Frame):
    """Oyun modu seçme ekranı."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        choose_mode_label = tk.Label(self, text="Hangi modu oynamak istiyorsunuz?",
                                     font=FONT_COURIER_BOLD, fg=COLOR_FG, bg=COLOR_BG,
                                     width=33, height=2, wraplength=400)
        choose_mode_label.pack(side="top", pady=(2, 20))

        tk.Button(self, width=10, height=2, text="Geri",
                  command=lambda: controller.show_frame("LanguageSelectScreen"),
                  bg=COLOR_BTN_BACK, fg="white").pack(side="bottom")

        tk.Button(self, text="Eşleştirme", fg=COLOR_BTN_FG, bg=COLOR_BTN_MATCH, width=30, height=2,
                  command=lambda: controller.show_frame("WordMatchingScreen")
                  ).pack(side="bottom", pady=10)

        tk.Button(self, text="Çoktan Seçmeli", fg=COLOR_BTN_FG, bg=COLOR_BTN_CHOICE, width=30, height=2,
                  command=lambda: controller.show_frame("MultipleChoiceScreen")
                  ).pack(side="bottom", pady=10)