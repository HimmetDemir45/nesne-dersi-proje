import tkinter as tk
from tkinter import messagebox
import random

# Sabit değerlerimizi constants.py dosyasından içe aktarıyoruz
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

        top_frame = tk.Frame(self, bg=COLOR_BG)
        top_frame.pack(fill="x", padx=5, pady=5)

        self.time_label = tk.Label(top_frame, text=f"Süre: {self.time}",
                                   font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.time_label.pack(side="left")

        self.skor_label = tk.Label(top_frame, text="Skor: 0",
                                   font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.skor_label.pack(side="right")

        self.top_answer_label = tk.Label(self, text="Kelime", font=FONT_NY_BOLD,
                                         height=3, width=30, relief="groove")
        self.top_answer_label.pack(side="top", pady=20)

        buttons_frame = tk.Frame(self, bg=COLOR_BG)
        buttons_frame.pack(pady=10)

        for _ in range(4):
            btn = tk.Button(buttons_frame, text="", font=FONT_NY_BOLD, height=2, width=20)
            btn.pack(side="top", pady=5, fill="x")
            self.answer_buttons.append(btn)

        tk.Button(self, text="Menüye Dön", command=lambda: controller.show_frame("MenuScreen"),
                  bg=COLOR_BTN_BACK, fg="white", height=2, width=10
                  ).pack(side="bottom", pady=10)


    def on_show(self):
        """Bu ekran her gösterildiğinde çağrılır."""
        self.time = 10
        self.skor_label.config(text=f"Skor: {self.controller.score}")
        self.time_label.config(text=f"Süre: {self.time}")

        if self.countdown_id:
            self.after_cancel(self.countdown_id)

        self.setup_question()
        self.start_countdown()

    def setup_question(self):
        """Yeni bir soru hazırlar ve butonları günceller."""
        data = self.controller.get_data()
        if data is None: return

        try:
            col1, col2 = self.controller.language_pair
            col1_words = data[col1].to_list()
            col2_words = data[col2].to_list()
        except KeyError:
            messagebox.showerror("Hata", f"CSV dosyasında '{col1}' veya '{col2}' sütunları bulunamadı.")
            self.controller.show_frame("LanguageSelectScreen")
            return

        random_word = random.choice(col1_words)
        self.true_answer = col2_words[col1_words.index(random_word)]

        self.top_answer_label.config(text=random_word)

        answers = [self.true_answer]
        while len(answers) < 4:
            wrong = random.choice(col2_words)
            if wrong != self.true_answer and wrong not in answers:
                answers.append(wrong)

        random.shuffle(answers)

        for i, answer in enumerate(answers):
            self.answer_buttons[i].config(
                text=answer,
                command=lambda ans=answer: self.is_true(ans),
                state="normal"
            )

    def start_countdown(self):
        """Geri sayımı başlatan metod."""
        if self.time > 0:
            self.time -= 1
            self.time_label.config(text=f"Süre: {self.time}")
            self.countdown_id = self.after(1000, self.start_countdown)
        else:
            messagebox.showinfo("Süre doldu", "Cevap verilmedi!")
            self.on_show()

    def is_true(self, selected_answer):
        """Verilen cevabın doğruluğunu kontrol eder."""
        self.after_cancel(self.countdown_id)

        for btn in self.answer_buttons:
            btn.config(state="disabled")

        if selected_answer == self.true_answer:
            self.controller.score += 5
            self.skor_label.config(text=f"Skor: {self.controller.score}")
            messagebox.showinfo("Sonuç", "Cevap doğru tebrikler!")
        else:
            messagebox.showinfo("Sonuç", f"Cevap yanlış! Doğru cevap: {self.true_answer}")

        self.after(1000, self.on_show)


class WordMatchingScreen(tk.Frame):
    """Kelime eşleştirme oyun ekranı."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        self.time = 20
        self.countdown_id = None
        self.selected_word = ""
        self.selected_button = None
        self.correct_matches = 0
        self.word_map = {}
        self.left_buttons = []
        self.right_buttons = []

        top_frame = tk.Frame(self, bg=COLOR_BG)
        top_frame.pack(fill="x", padx=5, pady=5)

        self.time_label = tk.Label(top_frame, text=f"Süre: {self.time}",
                                   font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.time_label.pack(side="left")

        self.skor_label = tk.Label(top_frame, text="Skor: 0",
                                   font=FONT_NY_BOLD, fg=COLOR_FG, bg=COLOR_BG)
        self.skor_label.pack(side="right")

        main_game_frame = tk.Frame(self, bg=COLOR_BG)
        main_game_frame.pack(fill="x", expand=True, pady=20)

        left_frame = tk.Frame(main_game_frame, bg=COLOR_BG)
        left_frame.pack(side="left", fill="x", expand=True, padx=10)

        right_frame = tk.Frame(main_game_frame, bg=COLOR_BG)
        right_frame.pack(side="right", fill="x", expand=True, padx=10)

        for i in range(4):
            left_btn = tk.Button(left_frame, text=f"L{i}", font=FONT_NY_BOLD, height=2, width=15)
            left_btn.pack(side="top", pady=10, fill="x")
            self.left_buttons.append(left_btn)

            right_btn = tk.Button(right_frame, text=f"R{i}", font=FONT_NY_BOLD, height=2, width=15)
            right_btn.pack(side="top", pady=10, fill="x")
            self.right_buttons.append(right_btn)

        tk.Button(self, text="Menüye Dön", command=lambda: controller.show_frame("MenuScreen"),
                  bg=COLOR_BTN_BACK, fg="white", height=2, width=10
                  ).pack(side="bottom", pady=10)


    def on_show(self):
        """Bu ekran her gösterildiğinde çağrılır."""
        self.time = 20
        self.correct_matches = 0
        self.selected_word = ""
        self.selected_button = None
        self.word_map = {}

        self.skor_label.config(text=f"Skor: {self.controller.score}")
        self.time_label.config(text=f"Süre: {self.time}")

        if self.countdown_id:
            self.after_cancel(self.countdown_id)

        self.setup_matches()
        self.start_countdown()

    def setup_matches(self):
        """Eşleştirme için 4 kelime çifti hazırlar."""
        data = self.controller.get_data()
        if data is None: return

        try:
            col1, col2 = self.controller.language_pair
            col1_words = data[col1].to_list()
            col2_words = data[col2].to_list()
        except KeyError:
            messagebox.showerror("Hata", f"CSV dosyasında '{col1}' veya '{col2}' sütunları bulunamadı.")
            self.controller.show_frame("LanguageSelectScreen")
            return

        random_words = []
        true_answers = []

        while len(random_words) < 4:
            word = random.choice(col1_words)
            if word not in random_words:
                random_words.append(word)
                answer = col2_words[col1_words.index(word)]
                true_answers.append(answer)
                self.word_map[word] = answer

        shuffled_answers = true_answers.copy()
        random.shuffle(shuffled_answers)

        for i in range(4):
            word = random_words[i]
            btn_left = self.left_buttons[i]
            btn_left.config(
                text=word,
                state="normal",
                command=lambda w=word, b=btn_left: self.select_word(w, b)
            )

            answer = shuffled_answers[i]
            btn_right = self.right_buttons[i]
            btn_right.config(
                text=answer,
                state="normal",
                command=lambda a=answer, b=btn_right: self.check_answer(a, b)
            )

    def start_countdown(self):
        """Geri sayımı başlatır."""
        if self.time > 0:
            self.time -= 1
            self.time_label.config(text=f"Süre: {self.time}")
            self.countdown_id = self.after(1000, self.start_countdown)
        else:
            messagebox.showinfo("Süre doldu", "Oyun bitti!")
            self.on_show()

    def select_word(self, word, button):
        """Sol taraftan bir kelime seçer."""
        if self.selected_button: # Zaten bir buton seçiliyse onu geri aç
            self.selected_button.config(state="normal")

        self.selected_word = word
        self.selected_button = button
        button.config(state="disabled")

    def check_answer(self, answer, button):
        """Sağ taraftan bir cevap seçer ve kontrol eder."""
        if not self.selected_word:
            messagebox.showwarning("Uyarı", "Lütfen önce soldan bir kelime seçin!")
            return

        true_answer = self.word_map[self.selected_word]

        if answer == true_answer:
            self.controller.score += 5
            self.correct_matches += 1
            self.skor_label.config(text=f"Skor: {self.controller.score}")

            button.config(state="disabled")
            messagebox.showinfo("Sonuç", "Cevap doğru tebrikler!")

        else:
            messagebox.showinfo("Sonuç", "Cevap yanlış!")
            if self.selected_button:
                self.selected_button.config(state="normal")

        self.selected_word = ""
        self.selected_button = None

        if self.correct_matches == 4:
            self.after_cancel(self.countdown_id)
            messagebox.showinfo("Tebrikler!", "Tüm kelimeleri eşleştirdiniz!")
            self.after(1000, self.on_show)