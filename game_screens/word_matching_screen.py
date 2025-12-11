import tkinter as tk
import random
from constants import *

class WordMatchingScreen(tk.Frame):
    """Kelime eşleştirme oyun ekranı."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        self.start_time = 60  # Genel süre (Saniye). Artık ekleme olmadığı için artırdık.
        self.time = self.start_time
        self.countdown_id = None

        # Oyun Durum Değişkenleri
        self.selected_word = ""
        self.selected_button = None
        self.correct_matches = 0
        self.word_map = {}
        self.left_buttons = []
        self.right_buttons = []
        self.is_game_active = False

        # --- Üst Panel (Süre ve Skor) ---
        top_frame = tk.Frame(self, bg=COLOR_BG)
        top_frame.pack(fill="x", padx=10, pady=5)

        self.time_label = tk.Label(top_frame, text=f"Süre: {self.time}",
                                   font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.time_label.pack(side="left")

        self.skor_label = tk.Label(top_frame, text="Skor: 0",
                                   font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.skor_label.pack(side="right")

        # --- Oyun Alanı (Sol ve Sağ Butonlar) ---
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
        # "Pes Et" butonu artık sonucu gösteriyor
        tk.Button(self, text="Pes Et / Bitir", command=self.go_back,
                  bg=COLOR_BTN_BACK, fg="white", height=2, width=15
                  ).pack(side="bottom", pady=10)

    def go_back(self):
        """Pes edince direkt menüye gitmek yerine sonucu göster."""
        self.finish_game()

    def stop_timer(self):
        """Sayacı güvenli şekilde durdurur."""
        if self.countdown_id:
            self.after_cancel(self.countdown_id)
            self.countdown_id = None

    def on_show(self):
        """Ekran her açıldığında oyunu sıfırla."""
        self.controller.score = 0
        self.start_new_game()

    def start_new_game(self):
        """Oyunu en baştan başlatır."""
        self.time = self.start_time
        self.correct_matches = 0
        self.selected_word = ""
        self.selected_button = None
        self.word_map = {}
        self.is_game_active = True

        # Etiketleri Güncelle
        self.skor_label.config(text=f"Skor: {self.controller.score}")
        self.time_label.config(text=f"Süre: {self.time}")

        self.stop_timer()
        self.setup_matches()
        self.start_timer()

    def prepare_next_round(self):
        """Tüm eşleşmeler bitince çalışır: Yeni kelimeler getirir."""
        self.correct_matches = 0
        self.selected_word = ""
        self.selected_button = None

        # GÜNCELLEME: Süre ekleme kodu kaldırıldı. Genel süre işleyecek.
        # self.time += 10 (SİLİNDİ)

        self.setup_matches()

    def setup_matches(self):
        """Kelimeleri hafızadan çeker ve butonlara yerleştirir."""
        data = self.controller.get_data()
        if data is None: return

        try:
            col1, col2 = self.controller.language_pair
            col1_words = data[col1].to_list()
            col2_words = data[col2].to_list()
        except KeyError:
            # Hata durumunda menüye dön (güvenli çıkış)
            self.controller.show_frame("MenuScreen")
            return

        # 4 Rastgele Çift Seç
        count = min(4, len(col1_words))
        indices = random.sample(range(len(col1_words)), count)

        current_words_left = []
        current_words_right = []
        self.word_map = {}

        for idx in indices:
            w1 = col1_words[idx]
            w2 = col2_words[idx]
            current_words_left.append(w1)
            current_words_right.append(w2)
            self.word_map[w1] = w2

            # Sağ tarafı karıştır
        random.shuffle(current_words_right)

        # Butonları ayarla
        for i in range(4):
            if i < count:
                text_left = current_words_left[i]
                text_right = current_words_right[i]
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
        """Sayacı başlatır."""
        self.stop_timer()
        self.countdown_id = self.after(1000, self.tick)

    def tick(self):
        """Her saniye çalışan sayaç döngüsü."""
        if not self.is_game_active: return

        if self.time > 0:
            self.time -= 1
            self.time_label.config(text=f"Süre: {self.time}")
            self.countdown_id = self.after(1000, self.tick)
        else:
            # Süre bitti -> Oyun Bitti
            self.finish_game()

    def select_left(self, word, button):
        """Sol taraftan kelime seçimi."""
        if not self.is_game_active: return

        if self.selected_button == button:
            button.config(bg="white")
            self.selected_button = None
            self.selected_word = ""
            return

        if self.selected_button:
            self.selected_button.config(bg="white")

        self.selected_word = word
        self.selected_button = button
        button.config(bg="#F1C40F") # Sarı

    def select_right(self, word, button):
        """Sağ taraftan kelime seçimi ve kontrol."""
        if not self.is_game_active or not self.selected_word:
            return

        true_answer = self.word_map.get(self.selected_word)

        if word == true_answer:
            # --- DOĞRU EŞLEŞME ---
            self.controller.score += 5
            self.correct_matches += 1
            self.skor_label.config(text=f"Skor: {self.controller.score}")

            # Butonları yeşil yap ve kapat
            self.selected_button.config(bg=COLOR_BTN_PLAY, state="disabled")
            button.config(bg=COLOR_BTN_PLAY, state="disabled")

            # Seçimi temizle
            self.selected_button = None
            self.selected_word = ""

            # Tüm eşleşmeler bitti mi?
            if self.correct_matches == 4:
                # 0.5 saniye bekle sonra yeni kelimeleri getir
                self.after(500, self.prepare_next_round)
        else:
            # --- YANLIŞ EŞLEŞME ---
            btn_left = self.selected_button
            btn_right = button

            # Kırmızı yap
            btn_left.config(bg="#E74C3C")
            btn_right.config(bg="#E74C3C")

            def reset_colors(b1, b2):
                if self.is_game_active:
                    if b1['state'] == 'normal': b1.config(bg="white")
                    if b2['state'] == 'normal': b2.config(bg="white")

            self.after(500, lambda: reset_colors(btn_left, btn_right))

            self.selected_button = None
            self.selected_word = ""

    def finish_game(self):
        """Oyun bitti, sonuç ekranına git."""
        self.is_game_active = False
        self.stop_timer()
        self.controller.show_frame("ResultScreen")