import tkinter as tk
from constants import *

class MultipleChoiceScreen(tk.Frame):
    """
    Artık sadece GÖRÜNÜM (View) işini yapar. Mantık GameEngine'dedir.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        # UI ile ilgili zamanlayıcı değişkenleri burada kalabilir
        self.time = 10
        self.countdown_id = None
        self.is_processing = False

        # --- UI Kurulumu (Değişmedi) ---
        top_frame = tk.Frame(self, bg=COLOR_BG)
        top_frame.pack(fill="x", padx=10, pady=10)

        self.counter_label = tk.Label(top_frame, text="Soru: 0/0", font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.counter_label.pack(side="left", padx=10)

        self.time_label = tk.Label(top_frame, text="Süre: 10", font=FONT_NY_BOLD, fg="#E74C3C", bg=COLOR_BG)
        self.time_label.pack(side="left", padx=20)

        self.skor_label = tk.Label(top_frame, text="Skor: 0", font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.skor_label.pack(side="right", padx=10)

        self.top_answer_label = tk.Label(self, text="...", font=("Arial", 24, "bold"),
                                         bg="white", fg="black", height=2, width=20, relief="solid")
        self.top_answer_label.pack(side="top", pady=30)

        buttons_frame = tk.Frame(self, bg=COLOR_BG)
        buttons_frame.pack(pady=10)

        self.answer_buttons = []
        for _ in range(4):
            btn = tk.Button(buttons_frame, text="", font=FONT_NY_BOLD, height=2, width=25, bg="white", fg="black")
            btn.pack(side="top", pady=5)
            self.answer_buttons.append(btn)

        tk.Button(self, text="Pes Et / Menü", command=self.finish_game,
                  bg=COLOR_BTN_BACK, fg="white", height=2, width=15).pack(side="bottom", pady=20)

    def on_show(self):
        """Oyun başladığında motoru tetikle."""
        self.stop_timer()
        self.is_processing = False

        # Motoru sıfırla
        self.controller.game_engine.start_new_game()

        # UI'ı sıfırla
        self.skor_label.config(text="Skor: 0")
        self.setup_question()

    def setup_question(self):
        """Motordan yeni soru iste."""
        # YENİ YAPI: GameEngine'den soru al
        q_data = self.controller.game_engine.generate_question()

        # Eğer soru gelmediyse (None), oyun bitmiştir
        if q_data is None:
            self.finish_game()
            return

        self.is_processing = False

        # UI Güncelleme
        self.counter_label.config(text=f"Soru: {q_data['q_number']}/{q_data['total']}")
        self.top_answer_label.config(text=q_data['question'])

        # Butonları ayarla
        for i, btn in enumerate(self.answer_buttons):
            option_text = q_data['options'][i]
            btn.config(text=option_text, bg="white", state="normal",
                       command=lambda ans=option_text, b=btn: self.check_answer(ans, b))

        # Süreyi başlat
        self.time = 10
        self.time_label.config(text=f"Süre: {self.time}")
        self.start_timer()

    def check_answer(self, selected_answer, btn):
        if self.is_processing: return
        self.is_processing = True
        self.stop_timer()

        # Butonları kilitle
        for b in self.answer_buttons:
            b.config(state="disabled")

        # YENİ YAPI: Cevabı motora sor
        is_correct, new_score = self.controller.game_engine.check_answer(selected_answer)

        # UI Güncelleme
        self.skor_label.config(text=f"Skor: {new_score}")

        if is_correct:
            btn.config(bg=COLOR_BTN_PLAY) # Yeşil
        else:
            btn.config(bg="#E74C3C") # Kırmızı
            # Doğru cevabı göster (View tarafında bulmak zorundayız veya motordan da isteyebilirdik)
            # Şimdilik basitçe butonları tarayıp doğruyu bulalım (GameEngine'de current_correct_answer'a erişim açabiliriz)
            correct_ans = self.controller.game_engine.current_correct_answer
            for b in self.answer_buttons:
                if b['text'] == correct_ans:
                    b.config(bg=COLOR_BTN_PLAY)

        self.after(1000, self.setup_question)

    # --- Timer Metotları (UI'a özgü olduğu için burada kalabilir) ---
    def start_timer(self):
        self.stop_timer()
        self.countdown_id = self.after(1000, self.tick)

    def tick(self):
        if self.is_processing: return
        if self.time > 0:
            self.time -= 1
            self.time_label.config(text=f"Süre: {self.time}")
            self.countdown_id = self.after(1000, self.tick)
        else:
            self.time_up()

    def stop_timer(self):
        if self.countdown_id:
            self.after_cancel(self.countdown_id)
            self.countdown_id = None

    def time_up(self):
        self.is_processing = True
        self.top_answer_label.config(text="Süre Doldu!")

        # Doğruyu göster
        correct_ans = self.controller.game_engine.current_correct_answer
        for b in self.answer_buttons:
            if b['text'] == correct_ans:
                b.config(bg=COLOR_BTN_PLAY)

        self.after(1500, self.setup_question)

    def finish_game(self):
        self.stop_timer()
        self.controller.show_frame("ResultScreen")