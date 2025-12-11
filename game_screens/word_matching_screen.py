import tkinter as tk
import random
from constants import *

class WordMatchingScreen(tk.Frame):
    """Kelime eşleştirme oyun ekranı."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        self.time = 20
        self.countdown_id = None
        self.selected_word = ""
        self.selected_button = None
        self.correct_matches = 0
        self.word_map = {}
        self.left_buttons = []
        self.right_buttons = []

        # Üst Panel
        top_frame = tk.Frame(self, bg=COLOR_BG)
        top_frame.pack(fill="x", padx=10, pady=5)

        self.time_label = tk.Label(top_frame, text=f"Süre: {self.time}",
                                   font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.time_label.pack(side="left")

        self.skor_label = tk.Label(top_frame, text="Skor: 0",
                                   font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.skor_label.pack(side="right")

        # Oyun Alanı
        main_game_frame = tk.Frame(self, bg=COLOR_BG)
        main_game_frame.pack(fill="x", expand=True, pady=20)

        left_frame = tk.Frame(main_game_frame, bg=COLOR_BG)
        left_frame.pack(side="left", fill="both", expand=True, padx=20)

        right_frame = tk.Frame(main_game_frame, bg=COLOR_BG)
        right_frame.pack(side="right", fill="both", expand=True, padx=20)

        for i in range(4):
            left_btn = tk.Button(left_frame, text="", font=FONT_NY_BOLD, height=2, bg="white")
            left_btn.pack(side="top", pady=8, fill="x")
            self.left_buttons.append(left_btn)

            right_btn = tk.Button(right_frame, text="", font=FONT_NY_BOLD, height=2, bg="white")
            right_btn.pack(side="top", pady=8, fill="x")
            self.right_buttons.append(right_btn)

        # Geri Dön
        tk.Button(self, text="Menüye Dön", command=self.go_back,
                  bg=COLOR_BTN_BACK, fg="white", height=2, width=15
                  ).pack(side="bottom", pady=10)

    def go_back(self):
        if self.countdown_id:
            self.after_cancel(self.countdown_id)
        self.controller.show_frame("MenuScreen")

    def on_show(self):
        self.time = 25 # Süreyi biraz artırdık
        self.correct_matches = 0
        self.selected_word = ""
        self.selected_button = None
        self.word_map = {}

        self.skor_label.config(text=f"Skor: {self.controller.score}")
        self.time_label.config(text=f"Süre: {self.time}")

        if self.countdown_id:
            self.after_cancel(self.countdown_id)

        self.setup_matches()
        self.start_countdown()

    def setup_matches(self):
        data = self.controller.get_data()
        if data is None: return

        try:
            col1, col2 = self.controller.language_pair
            col1_words = data[col1].to_list()
            col2_words = data[col2].to_list()
        except KeyError:
            self.go_back()
            return

        # 4 Rastgele kelime çifti seç
        indices = random.sample(range(len(col1_words)), min(4, len(col1_words)))

        current_words_left = []
        current_words_right = []
        self.word_map = {}

        for idx in indices:
            w1 = col1_words[idx]
            w2 = col2_words[idx]
            current_words_left.append(w1)
            current_words_right.append(w2)
            self.word_map[w1] = w2 # Eşleşme sözlüğü

        # Sağ tarafı karıştır
        random.shuffle(current_words_right)

        # Butonlara ata
        for i in range(4):
            # Sol
            self.left_buttons[i].config(text=current_words_left[i], state="normal", bg="white",
                                        command=lambda w=current_words_left[i], b=self.left_buttons[i]: self.select_left(w, b))
            # Sağ
            self.right_buttons[i].config(text=current_words_right[i], state="normal", bg="white",
                                         command=lambda w=current_words_right[i], b=self.right_buttons[i]: self.select_right(w, b))

    def start_countdown(self):
        if self.time > 0:
            self.time -= 1
            self.time_label.config(text=f"Süre: {self.time}")
            self.countdown_id = self.after(1000, self.start_countdown)
        else:
            # Süre dolunca otomatik yenile (veya oyun bitti ekranı yapılabilir)
            self.on_show()

    def select_left(self, word, button):
        """Sol taraftan seçim yapma."""
        # Eğer zaten seçiliyse iptal et
        if self.selected_button == button:
            button.config(bg="white")
            self.selected_button = None
            self.selected_word = ""
            return

        # Önceki seçimi temizle
        if self.selected_button:
            self.selected_button.config(bg="white")

        # Yeni seçim
        self.selected_word = word
        self.selected_button = button
        button.config(bg="#F1C40F") # Sarı (Seçildi)

    def select_right(self, word, button):
        """Sağ tarafa tıklayınca kontrol et."""
        if not self.selected_word:
            return # Soldan seçim yapılmamışsa tepki verme

        true_answer = self.word_map[self.selected_word]

        if word == true_answer:
            # DOĞRU EŞLEŞME
            self.controller.score += 5
            self.correct_matches += 1
            self.skor_label.config(text=f"Skor: {self.controller.score}")

            # İkisini de Yeşil yap ve devre dışı bırak
            self.selected_button.config(bg=COLOR_BTN_PLAY, state="disabled") # Sol
            button.config(bg=COLOR_BTN_PLAY, state="disabled") # Sağ

            # Seçimi sıfırla
            self.selected_button = None
            self.selected_word = ""

            # Hepsi bitti mi?
            if self.correct_matches == 4:
                self.after_cancel(self.countdown_id)
                self.after(1000, self.on_show) # 1 sn sonra yeni tur
        else:
            # YANLIŞ EŞLEŞME
            # Kısa süreliğine kırmızı yap
            orig_color_left = self.selected_button.cget("bg")

            self.selected_button.config(bg="#E74C3C")
            button.config(bg="#E74C3C")

            def reset_colors(b1, b2):
                b1.config(bg="white")
                b2.config(bg="white")

            # 0.5 sn sonra beyaz yap
            self.after(500, lambda: reset_colors(self.selected_button, button))

            # Seçimi sıfırla
            self.selected_button = None
            self.selected_word = ""