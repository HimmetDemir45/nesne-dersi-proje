import tkinter as tk
import random
from constants import *

class MultipleChoiceScreen(tk.Frame):
    """Çoktan seçmeli oyun ekranı."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        self.start_time = 10 # Her soru için süre
        self.total_questions = 10 # Toplam soru sayısı
        self.time = self.start_time
        self.countdown_id = None
        self.true_answer = ""
        self.answer_buttons = []
        self.is_processing = False
        self.question_count = 0

        # --- Üst Bilgi Paneli ---
        top_frame = tk.Frame(self, bg=COLOR_BG)
        top_frame.pack(fill="x", padx=10, pady=10)

        # Sol taraf: Soru Sayacı
        self.counter_label = tk.Label(top_frame, text=f"Soru: 1/{self.total_questions}",
                                      font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.counter_label.pack(side="left", padx=10)

        # Orta: Süre
        self.time_label = tk.Label(top_frame, text=f"Süre: {self.time}",
                                   font=FONT_NY_BOLD, fg="#E74C3C", bg=COLOR_BG) # Süre kırmızı renkte
        self.time_label.pack(side="left", padx=20)

        # Sağ: Skor
        self.skor_label = tk.Label(top_frame, text="Skor: 0",
                                   font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.skor_label.pack(side="right", padx=10)

        # --- Soru Alanı ---
        self.top_answer_label = tk.Label(self, text="...", font=("Arial", 24, "bold"),
                                         bg="white", fg="black", height=2, width=20, relief="solid")
        self.top_answer_label.pack(side="top", pady=30)

        # --- Şıklar ---
        buttons_frame = tk.Frame(self, bg=COLOR_BG)
        buttons_frame.pack(pady=10)

        for _ in range(4):
            btn = tk.Button(buttons_frame, text="", font=FONT_NY_BOLD, height=2, width=25,
                            bg="white", fg="black")
            btn.pack(side="top", pady=5)
            self.answer_buttons.append(btn)

        # Alt Buton
        tk.Button(self, text="Pes Et / Menü", command=self.go_back,
                  bg=COLOR_BTN_BACK, fg="white", height=2, width=15
                  ).pack(side="bottom", pady=20)

    def go_back(self):
        """Menüye dön."""
        self.finish_game()

    def stop_timer(self):
        """Sayacı durdurur."""
        if self.countdown_id:
            self.after_cancel(self.countdown_id)
            self.countdown_id = None

    def on_show(self):
        """Ekran açıldığında oyunu sıfırla ve başlat."""
        self.controller.score = 0
        self.question_count = 0
        self.skor_label.config(text=f"Skor: 0")
        self.is_processing = False
        self.stop_timer()
        self.setup_question()

    def setup_question(self):
        """Yeni soru hazırlar."""
        # 1. KONTROL: Eğer soru sayısı limit dolduysa oyunu bitir
        if self.question_count >= self.total_questions:
            self.finish_game()
            return

        # Soru sayısını artır ve etiketi güncelle
        self.question_count += 1
        self.counter_label.config(text=f"Soru: {self.question_count}/{self.total_questions}")

        # Veriyi al
        data = self.controller.get_data()
        if data is None: return

        self.is_processing = False

        # Süreyi sıfırla
        self.time = self.start_time
        self.time_label.config(text=f"Süre: {self.time}")

        # Butonları temizle
        for btn in self.answer_buttons:
            btn.config(bg="white", state="normal")

        try:
            col1, col2 = self.controller.language_pair
            col1_words = data[col1].to_list()
            col2_words = data[col2].to_list()
        except KeyError:
            self.go_back()
            return

        # Rastgele soru seç
        random_index = random.randint(0, len(col1_words) - 1)
        question_word = col1_words[random_index]
        self.true_answer = col2_words[random_index]

        self.top_answer_label.config(text=question_word)

        # Şıkları oluştur
        answers = [self.true_answer]
        while len(answers) < 4:
            wrong = random.choice(col2_words)
            if wrong != self.true_answer and wrong not in answers:
                answers.append(wrong)

        random.shuffle(answers)

        for i, answer in enumerate(answers):
            self.answer_buttons[i].config(
                text=answer,
                command=lambda ans=answer, b=self.answer_buttons[i]: self.check_answer(ans, b)
            )

        # Sayacı başlat
        self.start_timer()

    def start_timer(self):
        self.stop_timer()
        # 1 saniye bekle ve saymaya başla
        self.countdown_id = self.after(1000, self.tick)

    def tick(self):
        if self.is_processing: return

        if self.time > 0:
            self.time -= 1
            self.time_label.config(text=f"Süre: {self.time}")

            if self.time > 0:
                self.countdown_id = self.after(1000, self.tick)
            else:
                self.time_up()
        else:
            self.time_up()

    def time_up(self):
        """Bu soru için süre doldu."""
        self.is_processing = True
        self.top_answer_label.config(text="Süre Doldu!")
        self.show_correct_answer()
        # 1.5 saniye sonra yeni soruya geç
        self.after(1500, self.setup_question)

    def show_correct_answer(self):
        """Doğru cevabı yeşil yap."""
        for btn in self.answer_buttons:
            if btn['text'] == self.true_answer:
                btn.config(bg=COLOR_BTN_PLAY)

    def check_answer(self, selected_answer, btn):
        if self.is_processing: return
        self.is_processing = True
        self.stop_timer()

        for b in self.answer_buttons:
            b.config(state="disabled")

        if selected_answer == self.true_answer:
            btn.config(bg=COLOR_BTN_PLAY) # Yeşil
            self.controller.score += 5
            self.skor_label.config(text=f"Skor: {self.controller.score}")
        else:
            btn.config(bg="#E74C3C") # Kırmızı
            self.show_correct_answer()

        # 1 saniye sonra yeni soruya geç
        self.after(1000, self.setup_question)

    def finish_game(self):
        """Oyun bitti, sonuç ekranına git."""
        self.stop_timer()
        # Eğer app.py güncellenmediyse burada hata olabilir, kontrol edelim.
        try:
            self.controller.show_frame("ResultScreen")
        except KeyError:
            # Eğer ResultScreen eklenmemişse menüye dön
            print("Hata: ResultScreen bulunamadı. Lütfen app.py dosyasını güncelleyin.")
            self.controller.show_frame("MenuScreen")