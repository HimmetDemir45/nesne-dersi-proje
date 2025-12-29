import tkinter as tk
from ui.abstract_screen import AbstractScreen

class GameScreen(AbstractScreen):
    def create_widgets(self):
        # --- Üst Bilgi Paneli ---
        info_frame = tk.Frame(self, bg="#F0F3F4")
        info_frame.pack(fill="x", padx=20, pady=10)

        self.lbl_score = tk.Label(info_frame, text="Skor: 0", font=("Arial", 12, "bold"), bg="#F0F3F4")
        self.lbl_score.pack(side="right")

        self.lbl_question_count = tk.Label(info_frame, text="Soru: 1/10", font=("Arial", 12, "bold"), bg="#F0F3F4")
        self.lbl_question_count.pack(side="left")

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

        # Pes Et Butonu
        tk.Button(self, text="Pes Et", command=lambda: self.navigate("MenuScreen"),
                  bg="#E74C3C", fg="white").pack(side="bottom", pady=20)

        self.current_options = []
        self.processing = False

    def on_show(self):
        """Ekran her açıldığında yeni soruyla başla."""
        self.processing = False
        self.update_score_label()
        self.next_round()

    def next_round(self):
        """Controller'dan sıradaki soruyu iste."""
        q_data = self.controller.next_question()

        # Eğer soru gelmediyse oyun bitmiştir
        if q_data is None:
            # ResultScreen'e git (Onu da eklememiz gerekecek)
            # self.navigate("ResultScreen")
            print("Oyun Bitti! Skor:", self.controller.get_score())
            self.navigate("MenuScreen") # Şimdilik menüye atalım
            return

        # UI Güncelle
        self.lbl_question.config(text=q_data['question'])
        self.lbl_question_count.config(text=f"Soru: {q_data['index']}/{q_data['total']}")

        self.current_options = q_data['options']

        for i, btn in enumerate(self.buttons):
            btn.config(text=self.current_options[i], bg="white", state="normal")

        self.processing = False

    def check_answer(self, btn_index):
        if self.processing: return
        self.processing = True

        selected_text = self.current_options[btn_index]
        is_correct = self.controller.check_choice(selected_text)

        # Görsel Geri Bildirim
        btn = self.buttons[btn_index]
        if is_correct:
            btn.config(bg="#2ECC71") # Yeşil
        else:
            btn.config(bg="#E74C3C") # Kırmızı
            # Doğruyu göster
            # (Basitlik adına burada loop ile doğruyu bulup yeşil yapabiliriz)

        self.update_score_label()

        # 1 saniye sonra yeni soru
        self.after(1000, self.next_round)

    def update_score_label(self):
        score = self.controller.get_score()
        self.lbl_score.config(text=f"Skor: {score}")