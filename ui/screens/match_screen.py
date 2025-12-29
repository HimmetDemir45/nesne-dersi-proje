import tkinter as tk
from ui.abstract_screen import AbstractScreen

class MatchScreen(AbstractScreen):
    """
    Eşleştirme Oyunu Ekranı.
    Görünüm ve kullanıcı etkileşimini yönetir. Mantık Controller'dadır.
    """
    def create_widgets(self):
        # --- Üst Panel (Skor ve Süre) ---
        top_frame = tk.Frame(self, bg="#F0F3F4")
        top_frame.pack(fill="x", padx=10, pady=5)

        self.lbl_timer = tk.Label(top_frame, text="Süre: 60", font=("Arial", 12, "bold"), bg="#F0F3F4", fg="#E74C3C")
        self.lbl_timer.pack(side="left")

        self.lbl_score = tk.Label(top_frame, text="Skor: 0", font=("Arial", 12, "bold"), bg="#F0F3F4", fg="#2C3E50")
        self.lbl_score.pack(side="right")

        # --- Oyun Alanı (Sol ve Sağ Sütunlar) ---
        game_area = tk.Frame(self, bg="#F0F3F4")
        game_area.pack(fill="both", expand=True, pady=10)

        # Sol Sütun (Sorular)
        self.left_frame = tk.Frame(game_area, bg="#F0F3F4")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Sağ Sütun (Cevaplar)
        self.right_frame = tk.Frame(game_area, bg="#F0F3F4")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.left_buttons = []
        self.right_buttons = []

        # 4'er buton oluşturuyoruz
        for i in range(4):
            # Sol Buton
            btn_l = tk.Button(self.left_frame, text="", font=("Arial", 10, "bold"), height=2, bg="white", width=20)
            btn_l.pack(pady=10) # Dikey boşluk
            self.left_buttons.append(btn_l)

            # Sağ Buton
            btn_r = tk.Button(self.right_frame, text="", font=("Arial", 10, "bold"), height=2, bg="white", width=20)
            btn_r.pack(pady=10)
            self.right_buttons.append(btn_r)

        # --- Alt Panel (Pes Et) ---
        tk.Button(self, text="Pes Et / Bitir", command=self.finish_game,
                  bg="#95A5A6", fg="white", font=("Arial", 10, "bold"), width=15
                  ).pack(side="bottom", pady=20)

        # Oyun Durum Değişkenleri
        self.selected_left_word = None
        self.selected_left_btn = None
        self.matches_found = 0
        self.timer_id = None
        self.time_left = 60

    def on_show(self):
        """Ekran açıldığında oyunu başlat."""
        self.matches_found = 0
        self.lbl_score.config(text=f"Skor: {self.controller.get_score()}")
        self.start_new_round()
        self.start_timer()

    def start_new_round(self):
        """Controller'dan yeni kelime çiftlerini iste."""
        data = self.controller.next_match_round()

        # Eğer veri yoksa veya hata varsa oyunu bitir
        if not data:
            self.finish_game()
            return

        left_words = data['left']
        right_words = data['right']

        count = len(left_words)

        # Butonları güncelle
        for i in range(4):
            l_btn = self.left_buttons[i]
            r_btn = self.right_buttons[i]

            if i < count:
                # Sol Buton Ayarları
                l_text = left_words[i]
                l_btn.config(text=l_text, state="normal", bg="white",
                             command=lambda w=l_text, b=l_btn: self.select_left(w, b))

                # Sağ Buton Ayarları
                r_text = right_words[i]
                r_btn.config(text=r_text, state="normal", bg="white",
                             command=lambda w=r_text, b=r_btn: self.select_right(w, b))
            else:
                # Fazla butonları gizle/pasif yap
                l_btn.config(state="disabled", text="", bg="#F0F3F4", relief="flat")
                r_btn.config(state="disabled", text="", bg="#F0F3F4", relief="flat")

    def select_left(self, word, btn):
        """Sol sütundan seçim yapıldığında."""
        # Eğer zaten seçili bir buton varsa rengini sıfırla
        if self.selected_left_btn:
            self.selected_left_btn.config(bg="white")

        self.selected_left_word = word
        self.selected_left_btn = btn
        btn.config(bg="#F1C40F") # Sarı (Seçildiğini belli et)

    def select_right(self, word, btn):
        """Sağ sütundan seçim yapıldığında (Eşleştirme Kontrolü)."""
        if not self.selected_left_word:
            return # Sol seçilmeden sağa basılırsa işlem yapma

        # Controller'a sor: Bu ikisi eşleşiyor mu?
        is_correct = self.controller.check_match(self.selected_left_word, word)

        if is_correct:
            # --- DOĞRU ---
            # Yeşil yap ve kilitle
            self.selected_left_btn.config(bg="#2ECC71", state="disabled")
            btn.config(bg="#2ECC71", state="disabled")

            self.matches_found += 1
            self.lbl_score.config(text=f"Skor: {self.controller.get_score()}")

            # Seçimi temizle
            self.selected_left_word = None
            self.selected_left_btn = None

            # Tur bitti mi?
            if self.matches_found == 4:
                # Yarım saniye bekle, sonra yeni kelimeleri getir
                self.after(500, lambda: [self.reset_selection(), self.start_new_round(), setattr(self, 'matches_found', 0)])

        else:
            # --- YANLIŞ ---
            # Kırmızı yap
            btn.config(bg="#E74C3C")
            self.selected_left_btn.config(bg="#E74C3C")

            # Seçimi geçici olarak sakla (lambda içinde kaybolmasın diye)
            wrong_left_btn = self.selected_left_btn
            wrong_right_btn = btn

            # Yarım saniye sonra beyaz yap
            self.after(500, lambda: [
                wrong_right_btn.config(bg="white") if wrong_right_btn['state'] == 'normal' else None,
                wrong_left_btn.config(bg="white") if wrong_left_btn['state'] == 'normal' else None
            ])

            self.reset_selection()

    def reset_selection(self):
        self.selected_left_word = None
        self.selected_left_btn = None

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
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.navigate("ResultScreen")