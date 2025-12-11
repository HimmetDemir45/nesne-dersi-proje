import tkinter as tk
import random
from constants import *

class MultipleChoiceScreen(tk.Frame):
    """Çoktan seçmeli oyun ekranı."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        self.time = 10
        self.countdown_id = None
        self.true_answer = ""
        self.answer_buttons = []
        self.is_processing = False  # Cevap kontrolü sırasında tıklamayı engellemek için

        # Üst Bilgi Paneli
        top_frame = tk.Frame(self, bg=COLOR_BG)
        top_frame.pack(fill="x", padx=10, pady=10)

        self.time_label = tk.Label(top_frame, text=f"Süre: {self.time}",
                                   font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.time_label.pack(side="left")

        self.skor_label = tk.Label(top_frame, text="Skor: 0",
                                   font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.skor_label.pack(side="right")

        # Soru Alanı
        self.top_answer_label = tk.Label(self, text="...", font=("Arial", 24, "bold"),
                                         bg="white", fg="black", height=2, width=20, relief="solid")
        self.top_answer_label.pack(side="top", pady=30)

        # Şıklar (Butonlar)
        buttons_frame = tk.Frame(self, bg=COLOR_BG)
        buttons_frame.pack(pady=10)

        for _ in range(4):
            btn = tk.Button(buttons_frame, text="", font=FONT_NY_BOLD, height=2, width=25,
                            bg="white", fg="black") # Varsayılan renkler
            btn.pack(side="top", pady=5)
            self.answer_buttons.append(btn)

        # Geri Dön Butonu
        tk.Button(self, text="Menüye Dön", command=self.go_back,
                  bg=COLOR_BTN_BACK, fg="white", height=2, width=15
                  ).pack(side="bottom", pady=20)

    def go_back(self):
        """Geri sayımı durdur ve menüye dön."""
        if self.countdown_id:
            self.after_cancel(self.countdown_id)
        self.controller.show_frame("MenuScreen")

    def on_show(self):
        """Ekran açıldığında sıfırla ve başlat."""
        self.time = 10
        self.skor_label.config(text=f"Skor: {self.controller.score}")
        self.time_label.config(text=f"Süre: {self.time}")
        self.is_processing = False

        if self.countdown_id:
            self.after_cancel(self.countdown_id)

        self.setup_question()
        self.start_countdown()

    def setup_question(self):
        """Yeni soru hazırla."""
        # Main dosyasındaki hafızaya alınmış veriyi kullan
        data = self.controller.get_data()
        if data is None:
            return

        self.is_processing = False
        self.time = 10
        self.time_label.config(text=f"Süre: {self.time}")

        # Buton renklerini sıfırla
        for btn in self.answer_buttons:
            btn.config(bg="white", state="normal")

        try:
            col1, col2 = self.controller.language_pair
            # Veriyi listeye çevir
            col1_words = data[col1].to_list()
            col2_words = data[col2].to_list()
        except KeyError:
            # Hata durumunda menüye at
            self.go_back()
            return

        # Rastgele kelime seç
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

    def start_countdown(self):
        """Süre sayacı."""
        if self.is_processing: return # Cevap kontrol ediliyorsa sayma

        if self.time > 0:
            self.time -= 1
            self.time_label.config(text=f"Süre: {self.time}")
            self.countdown_id = self.after(1000, self.start_countdown)
        else:
            # Süre doldu
            self.top_answer_label.config(text="Süre Doldu!")
            self.is_processing = True
            # Doğru cevabı göster (Yeşil yap)
            for btn in self.answer_buttons:
                if btn['text'] == self.true_answer:
                    btn.config(bg=COLOR_BTN_PLAY) # Yeşil
            # 1.5 sn sonra yeni soru
            self.after(1500, self.setup_question)
            # Sayacı tekrar başlatma, setup_question başlatacak

    def check_answer(self, selected_answer, btn):
        """Cevabı görsel olarak kontrol et."""
        if self.is_processing: return
        self.is_processing = True

        # Butonları geçici olarak dondur
        for b in self.answer_buttons:
            b.config(state="disabled")

        if selected_answer == self.true_answer:
            # DOĞRU: Yeşil yap, puan ekle
            btn.config(bg=COLOR_BTN_PLAY) # Yeşil
            self.controller.score += 5
            self.skor_label.config(text=f"Skor: {self.controller.score}")
        else:
            # YANLIŞ: Kırmızı yap
            btn.config(bg="#E74C3C") # Kırmızı
            # Doğru olanı da yeşil göster ki kullanıcı öğrensin
            for b in self.answer_buttons:
                if b['text'] == self.true_answer:
                    b.config(bg=COLOR_BTN_PLAY)

        # 1 saniye bekle ve yeni soruya geç
        self.after(1000, self.setup_question)