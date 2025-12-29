import tkinter as tk
from ui.abstract_screen import AbstractScreen

class MatchScreen(AbstractScreen):
    def create_widgets(self):
        # --- Üst Panel ---
        top_frame = tk.Frame(self, bg="#F0F3F4")
        top_frame.pack(fill="x", padx=10, pady=5)

        self.lbl_score = tk.Label(top_frame, text="Skor: 0", font=("Arial", 12, "bold"), bg="#F0F3F4")
        self.lbl_score.pack(side="right")

        self.lbl_timer = tk.Label(top_frame, text="Süre: 60", font=("Arial", 12, "bold"), bg="#F0F3F4")
        self.lbl_timer.pack(side="left")

        # --- Oyun Alanı (Sol ve Sağ) ---
        game_area = tk.Frame(self, bg="#F0F3F4")
        game_area.pack(fill="both", expand=True, pady=10)

        self.left_frame = tk.Frame(game_area, bg="#F0F3F4")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10)

        self.right_frame = tk.Frame(game_area, bg="#F0F3F4")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.left_buttons = []
        self.right_buttons = []

        # 4'er buton oluştur
        for i in range(4):
            btn_l = tk.Button(self.left_frame, text="", font=("Arial", 10), height=2, bg="white")
            btn_l.pack(fill="x", pady=5)
            self.left_buttons.append(btn_l)

            btn_r = tk.Button(self.right_frame, text="", font=("Arial", 10), height=2, bg="white")
            btn_r.pack(fill="x", pady=5)
            self.right_buttons.append(btn_r)

        # Alt Panel
        tk.Button(self, text="Bitir", command=self.finish_game,
                  bg="#E74C3C", fg="white").pack(side="bottom", pady=10)

        # State Değişkenleri
        self.selected_left = None
        self.selected_left_btn = None
        self.matches_found = 0
        self.timer_id = None
        self.time_left = 60

    def on_show(self):
        self.matches_found = 0
        self.start_new_round()
        self.start_timer()

    def start_new_round(self):
        # Controller'dan veriyi al
        data = self.controller.next_match_round()
        if not data:
            self.finish_game()
            return

        left_words = data['left']
        right_words = data['right']

        # Butonları doldur
        for i in range(4):
            if i < len(left_words):
                # Sol Buton
                l_text = left_words[i]
                self.left_buttons[i].config(text=l_text, state="normal", bg="white",
                                            command=lambda w=l_text, b=self.left_buttons[i]: self.select_left(w, b))

                # Sağ Buton
                r_text = right_words[i]
                self.right_buttons[i].config(text=r_text, state="normal", bg="white",
                                             command=lambda w=r_text, b=self.right_buttons[i]: self.select_right(w, b))
            else:
                self.left_buttons[i].config(state="disabled", text="")
                self.right_buttons[i].config(state="disabled", text="")

    def select_left(self, word, btn):
        # Önceki seçimi temizle
        if self.selected_left_btn:
            self.selected_left_btn.config(bg="white")

        self.selected_left = word
        self.selected_left_btn = btn
        btn.config(bg="#F1C40F") # Sarı (Seçildi)

    def select_right(self, word, btn):
        if not self.selected_left: return

        # Controller'a sor: Eşleşme doğru mu?
        is_correct = self.controller.check_match(self.selected_left, word)

        if is_correct:
            # Görsel Güncelleme (Yeşil)
            self.selected_left_btn.config(bg="#2ECC71", state="disabled")
            btn.config(bg="#2ECC71", state="disabled")
            self.matches_found += 1
            self.update_score()

            # Hepsi bitti mi?
            if self.matches_found == 4:
                self.after(500, lambda: [self.reset_selection(), self.start_new_round()])
            else:
                self.reset_selection()
        else:
            # Yanlış (Kırmızı)
            orig_bg = btn.cget("bg")
            btn.config(bg="#E74C3C")
            self.selected_left_btn.config(bg="#E74C3C")

            self.after(500, lambda: [
                btn.config(bg="white"),
                self.selected_left_btn.config(bg="white") if self.selected_left_btn else None,
                self.reset_selection()
            ])

    def reset_selection(self):
        self.selected_left = None
        self.selected_left_btn = None

    def update_score(self):
        self.lbl_score.config(text=f"Skor: {self.controller.get_score()}")

    def start_timer(self):
        self.time_left = 60
        self.tick()

    def tick(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.lbl_timer.config(text=f"Süre: {self.time_left}")
            self.timer_id = self.after(1000, self.tick)
        else:
            self.finish_game()

    def finish_game(self):
        if self.timer_id: self.after_cancel(self.timer_id)
        self.navigate("ResultScreen")