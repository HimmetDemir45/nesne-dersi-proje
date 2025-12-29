import tkinter as tk
from ui.abstract_screen import AbstractScreen

class MatchScreen(AbstractScreen):
    """
    Eşleştirme Oyunu Ekranı.
    """
    def create_widgets(self):
        # --- ANA KONTEYNER (Ortalamak için) ---
        center_frame = tk.Frame(self, bg="#F0F3F4")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # --- Üst Panel (Skor ve Süre ve Tur Bilgisi) ---
        top_frame = tk.Frame(center_frame, bg="#F0F3F4")
        top_frame.pack(fill="x", pady=(0, 20))

        self.lbl_timer = tk.Label(top_frame, text="60", font=("Arial", 16, "bold"), bg="#F0F3F4", fg="#E74C3C")
        self.lbl_timer.pack(side="left", padx=10)

        self.lbl_round = tk.Label(top_frame, text="Tur: 1/10", font=("Arial", 12, "bold"), bg="#F0F3F4")
        self.lbl_round.pack(side="left", padx=20)

        self.lbl_score = tk.Label(top_frame, text="Skor: 0", font=("Arial", 12, "bold"), bg="#F0F3F4", fg="#2C3E50")
        self.lbl_score.pack(side="right", padx=10)

        # --- Oyun Alanı (Sol ve Sağ Sütunlar) ---
        game_area = tk.Frame(center_frame, bg="#F0F3F4")
        game_area.pack()

        # Sol Sütun
        self.left_frame = tk.Frame(game_area, bg="#F0F3F4")
        self.left_frame.pack(side="left", padx=20)

        # Sağ Sütun
        self.right_frame = tk.Frame(game_area, bg="#F0F3F4")
        self.right_frame.pack(side="right", padx=20)

        self.left_buttons = []
        self.right_buttons = []

        # 4'er buton oluştur
        for i in range(4):
            btn_l = tk.Button(self.left_frame, text="", font=("Arial", 11), height=2, bg="white", width=18)
            btn_l.pack(pady=8)
            self.left_buttons.append(btn_l)

            btn_r = tk.Button(self.right_frame, text="", font=("Arial", 11), height=2, bg="white", width=18)
            btn_r.pack(pady=8)
            self.right_buttons.append(btn_r)

        # --- Alt Panel (Pes Et) ---
        tk.Button(center_frame, text="Pes Et / Bitir", command=self.give_up,
                  bg="#E74C3C", fg="white", font=("Arial", 10, "bold"), width=20
                  ).pack(pady=30)

        # Değişkenler
        self.selected_left_word = None
        self.selected_left_btn = None
        self.matches_found = 0
        self.timer_id = None
        self.time_left = 60

    def on_show(self):
        self.matches_found = 0
        self.lbl_score.config(text=f"Skor: {self.controller.get_score()}")
        self.start_new_round()

    def give_up(self):
        """Pes edince sonucu göster."""
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.navigate("ResultScreen")

    def start_new_round(self):
        """Yeni turu başlat ve süreyi sıfırla."""
        data = self.controller.next_match_round()

        if not data:
            self.give_up()
            return

        # UI Güncelle
        self.lbl_round.config(text=f"Tur: {data.get('round', 1)}/{data.get('total_rounds', 10)}")

        left_words = data['left']
        right_words = data['right']
        count = len(left_words)

        for i in range(4):
            l_btn = self.left_buttons[i]
            r_btn = self.right_buttons[i]

            if i < count:
                l_text = left_words[i]
                l_btn.config(text=l_text, state="normal", bg="white",
                             command=lambda w=l_text, b=l_btn: self.select_left(w, b))

                r_text = right_words[i]
                r_btn.config(text=r_text, state="normal", bg="white",
                             command=lambda w=r_text, b=r_btn: self.select_right(w, b))
            else:
                l_btn.config(state="disabled", text="", bg="#F0F3F4", relief="flat")
                r_btn.config(state="disabled", text="", bg="#F0F3F4", relief="flat")

        # Her turda süreyi 60 saniyeden tekrar başlat
        self.start_timer()

    def select_left(self, word, btn):
        if self.selected_left_btn:
            self.selected_left_btn.config(bg="white")

        self.selected_left_word = word
        self.selected_left_btn = btn
        btn.config(bg="#F1C40F") # Sarı

    def select_right(self, word, btn):
        if not self.selected_left_word:
            return

        is_correct = self.controller.check_match(self.selected_left_word, word)

        if is_correct:
            # --- DOĞRU ---
            self.selected_left_btn.config(bg="#2ECC71", state="disabled") # Yeşil
            btn.config(bg="#2ECC71", state="disabled")

            self.matches_found += 1
            self.lbl_score.config(text=f"Skor: {self.controller.get_score()}")

            self.selected_left_word = None
            self.selected_left_btn = None

            if self.matches_found == 4:
                # Tur bitince biraz bekle sonra yeni tur
                self.after(500, lambda: [self.reset_selection(), self.start_new_round(), setattr(self, 'matches_found', 0)])

        else:
            # --- YANLIŞ ---
            btn.config(bg="#E74C3C") # Kırmızı
            self.selected_left_btn.config(bg="#E74C3C")

            wrong_left = self.selected_left_btn
            wrong_right = btn

            self.after(500, lambda: [
                wrong_right.config(bg="white") if wrong_right['state'] == 'normal' else None,
                wrong_left.config(bg="white") if wrong_left['state'] == 'normal' else None
            ])

            self.reset_selection()

    def reset_selection(self):
        self.selected_left_word = None
        self.selected_left_btn = None

    def start_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.time_left = 15 # Her turda 15 sn
        self.tick()

    def tick(self):
        if self.time_left > 0:
            self.lbl_timer.config(text=str(self.time_left))
            self.time_left -= 1
            self.timer_id = self.after(1000, self.tick)
        else:
            # Süre biterse oyun biter
            self.give_up()