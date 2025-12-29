import tkinter as tk
from constants import *

class WordMatchingScreen(tk.Frame):
    """
    Kelime eşleştirme oyun ekranı.
    Mantık GameEngine sınıfına taşındı.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        self.start_time = 60
        self.time = self.start_time
        self.countdown_id = None

        # UI Durum Değişkenleri
        self.selected_word = ""
        self.selected_button = None
        self.correct_matches = 0
        self.left_buttons = []
        self.right_buttons = []
        self.is_game_active = False

        # --- Üst Panel ---
        top_frame = tk.Frame(self, bg=COLOR_BG)
        top_frame.pack(fill="x", padx=10, pady=5)

        self.time_label = tk.Label(top_frame, text=f"Süre: {self.time}",
                                   font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.time_label.pack(side="left")

        self.skor_label = tk.Label(top_frame, text="Skor: 0",
                                   font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.skor_label.pack(side="right")

        # --- Oyun Alanı ---
        main_game_frame = tk.Frame(self, bg=COLOR_BG)
        main_game_frame.pack(fill="x", expand=True, pady=20)

        left_frame = tk.Frame(main_game_frame, bg=COLOR_BG)
        left_frame.pack(side="left", fill="both", expand=True, padx=20)

        right_frame = tk.Frame(main_game_frame, bg=COLOR_BG)
        right_frame.pack(side="right", fill="both", expand=True, padx=20)

        for i in range(4):
            # Sol Butonlar
            left_btn = tk.Button(left_frame, text="", font=FONT_NY_BOLD, height=2, bg="white")
            left_btn.pack(side="top", pady=8, fill="x")
            self.left_buttons.append(left_btn)

            # Sağ Butonlar
            right_btn = tk.Button(right_frame, text="", font=FONT_NY_BOLD, height=2, bg="white")
            right_btn.pack(side="top", pady=8, fill="x")
            self.right_buttons.append(right_btn)

        # --- Alt Panel ---
        tk.Button(self, text="Pes Et / Bitir", command=self.go_back,
                  bg=COLOR_BTN_BACK, fg="white", height=2, width=15
                  ).pack(side="bottom", pady=10)

    def go_back(self):
        self.finish_game()

    def stop_timer(self):
        if self.countdown_id:
            self.after_cancel(self.countdown_id)
            self.countdown_id = None

    def on_show(self):
        """Ekran açılınca motoru ve arayüzü hazırla."""
        # Motoru başlat (Puan sıfırlanır, liste yüklenir)
        self.controller.game_engine.start_new_game()

        self.skor_label.config(text="Skor: 0")
        self.start_new_round()

    def start_new_round(self):
        """Oyunu başlatır."""
        self.time = self.start_time
        self.correct_matches = 0
        self.selected_word = ""
        self.selected_button = None
        self.is_game_active = True

        self.time_label.config(text=f"Süre: {self.time}")
        self.stop_timer()

        # Kelimeleri getir
        self.setup_matches()

        self.start_timer()

    def prepare_next_round(self):
        """Tüm eşleşmeler bitince yeni kelimeler getir."""
        self.correct_matches = 0
        self.selected_word = ""
        self.selected_button = None
        self.setup_matches()

    def setup_matches(self):
        """Motordan kelime çiftlerini ister ve butonlara basar."""
        # YENİ YAPI: GameEngine'den veri al
        match_data = self.controller.game_engine.generate_matches()

        if match_data is None:
            self.controller.show_frame("MenuScreen")
            return

        words_left = match_data["left"]
        words_right = match_data["right"]
        count = len(words_left)

        for i in range(4):
            if i < count:
                text_left = words_left[i]
                text_right = words_right[i]
                state = "normal"
            else:
                text_left = ""
                text_right = ""
                state = "disabled"

            # Sol Butonlar
            self.left_buttons[i].config(text=text_left, state=state, bg="white",
                                        command=lambda w=text_left, b=self.left_buttons[i]: self.select_left(w, b))
            # Sağ Butonlar
            self.right_buttons[i].config(text=text_right, state=state, bg="white",
                                         command=lambda w=text_right, b=self.right_buttons[i]: self.select_right(w, b))

    def start_timer(self):
        self.stop_timer()
        self.countdown_id = self.after(1000, self.tick)

    def tick(self):
        if not self.is_game_active: return

        if self.time > 0:
            self.time -= 1
            self.time_label.config(text=f"Süre: {self.time}")
            self.countdown_id = self.after(1000, self.tick)
        else:
            self.finish_game()

    def select_left(self, word, button):
        if not self.is_game_active: return

        # Aynı butona tekrar basılırsa seçimi kaldır
        if self.selected_button == button:
            button.config(bg="white")
            self.selected_button = None
            self.selected_word = ""
            return

        # Önceki seçimi temizle
        if self.selected_button:
            self.selected_button.config(bg="white")

        self.selected_word = word
        self.selected_button = button
        button.config(bg="#F1C40F") # Sarı

    def select_right(self, word, button):
        """Sağ taraftan seçim ve kontrol."""
        if not self.is_game_active or not self.selected_word:
            return

        # YENİ YAPI: Kontrolü GameEngine yapar
        is_correct, new_score = self.controller.game_engine.check_match_pair(self.selected_word, word)

        # Skoru güncelle
        self.skor_label.config(text=f"Skor: {new_score}")

        if is_correct:
            # --- DOĞRU ---
            self.correct_matches += 1

            # Görsel Güncelleme
            self.selected_button.config(bg=COLOR_BTN_PLAY, state="disabled") # Yeşil
            button.config(bg=COLOR_BTN_PLAY, state="disabled")

            self.selected_button = None
            self.selected_word = ""

            # Hepsi bitti mi?
            if self.correct_matches == 4:
                self.after(500, self.prepare_next_round)
        else:
            # --- YANLIŞ ---
            btn_left = self.selected_button
            btn_right = button

            btn_left.config(bg="#E74C3C") # Kırmızı
            btn_right.config(bg="#E74C3C")

            def reset_colors(b1, b2):
                if self.is_game_active:
                    if b1['state'] == 'normal': b1.config(bg="white")
                    if b2['state'] == 'normal': b2.config(bg="white")

            self.after(500, lambda: reset_colors(btn_left, btn_right))

            self.selected_button = None
            self.selected_word = ""

    def finish_game(self):
        self.is_game_active = False
        self.stop_timer()
        self.controller.show_frame("ResultScreen")