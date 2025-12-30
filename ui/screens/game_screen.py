import tkinter as tk
from ui.abstract_screen import AbstractScreen

class GameScreen(AbstractScreen):
    def create_widgets(self):
        # --- Üst Bilgi Paneli ---
        info_frame = tk.Frame(self, bg="#F0F3F4")
        info_frame.pack(fill="x", padx=20, pady=10)

        self.lbl_score = tk.Label(info_frame, text="Skor: 0", font=("Arial", 12, "bold"), bg="#F0F3F4")
        self.lbl_score.pack(side="right")

        # Soru sayacı
        self.lbl_question_count = tk.Label(info_frame, text="Soru: 1/10", font=("Arial", 12, "bold"), bg="#F0F3F4")
        self.lbl_question_count.pack(side="left", padx=(0, 20))

        # --- ZAMANLAYICI ---
        self.lbl_timer = tk.Label(info_frame, text="10", font=("Arial", 14, "bold"), fg="#E74C3C", bg="#F0F3F4")
        self.lbl_timer.pack(side="left")

        # --- Soru Alanı ---
        self.lbl_question = tk.Label(self, text="...", font=("Helvetica", 24, "bold"),
                                     bg="white", relief="solid", width=20, height=2)
        self.lbl_question.pack(pady=40)

        # --- Şıklar ---
        self.buttons = []
        btn_frame = tk.Frame(self, bg="#F0F3F4")
        btn_frame.pack(pady=10)

        for i in range(4):
            btn = tk.Button(btn_frame, text="", font=("Arial", 12), width=30, height=2,
                            bg="white", command=lambda idx=i: self.check_answer(idx))
            btn.pack(pady=5)
            self.buttons.append(btn)


        tk.Button(self, text="Pes Et", command=self.give_up,
                  bg="#E74C3C", fg="white").pack(side="bottom", pady=20)

        self.current_options = []
        self.current_correct_text = "" # Doğru cevabı burada tutacağız
        self.processing = False
        self.timer_id = None
        self.time_left = 10

    def give_up(self):
        """Pes et butonuna basılınca çalışır."""

        if hasattr(self, 'stop_timer'):
            self.stop_timer()

        print("Oyuncu pes etti.")
        self.navigate("ResultScreen")

    def on_show(self):
        """Ekran her açıldığında yeni oyun başlat."""
        self.processing = False
        self.update_score_label()
        self.next_round()

    def next_round(self):
        """Sıradaki soruyu getir ve zamanlayıcıyı başlat."""
        q_data = self.controller.next_question()

        if q_data is None:
            print("Oyun Bitti! Skor:", self.controller.get_score())
            self.navigate("ResultScreen")
            return

        # UI Güncelle
        self.lbl_question.config(text=q_data['question'])
        self.lbl_question_count.config(text=f"Soru: {q_data['index']}/{q_data['total']}")

        self.current_options = q_data['options']
        self.current_correct_text = q_data['correct'] # Doğru cevabı kaydet

        for i, btn in enumerate(self.buttons):
            btn.config(text=self.current_options[i], bg="white", state="normal")

        self.processing = False
        self.start_timer() # Süreyi başlat

    def start_timer(self):
        """10 saniyelik geri sayımı başlatır."""
        self.stop_timer() # Varsa eski sayacı durdur
        self.time_left = 10
        self.lbl_timer.config(text=str(self.time_left))
        self.countdown()

    def countdown(self):
        """Saniyeyi azaltır ve 0 olunca süreyi bitirir."""
        if self.processing: return # Cevap verildiyse dur

        if self.time_left > 0:
            self.lbl_timer.config(text=str(self.time_left))
            self.time_left -= 1
            self.timer_id = self.after(1000, self.countdown)
        else:
            self.lbl_timer.config(text="0")
            self.time_up()

    def stop_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    def time_up(self):
        """Süre dolunca yapılacaklar (Yanlış sayılır)."""
        if self.processing: return
        self.processing = True

        # Doğru cevabı gösterip geç
        self.show_correct_answer()
        self.after(1500, self.next_round)

    def check_answer(self, btn_index):
        if self.processing: return
        self.processing = True
        self.stop_timer() # Süreyi durdur

        selected_text = self.current_options[btn_index]
        # Controller üzerinden kontrol et (Puan ekleme orada yapılıyor)
        is_correct = self.controller.check_choice(selected_text)

        # --- GÖRSEL GERİ BİLDİRİM ---
        selected_btn = self.buttons[btn_index]

        if is_correct:
            selected_btn.config(bg="#2ECC71") # Yeşil
        else:
            selected_btn.config(bg="#E74C3C") # Yanlışsa Kırmızı
            self.show_correct_answer() # VE DOĞRU OLANI YEŞİL YAP

        self.update_score_label()

        # 0.5 saniye sonra yeni soru
        self.after(500, self.next_round)

    def show_correct_answer(self):
        """Şıklar arasında doğru olanı bulup yeşil yapar."""
        for btn in self.buttons:
            if btn.cget("text") == self.current_correct_text:
                btn.config(bg="#2ECC71")
                break

    def update_score_label(self):
        score = self.controller.get_score()
        self.lbl_score.config(text=f"Skor: {score}")