import tkinter as tk
from tkinter import messagebox
import requests
import threading
import time
import pygame

pygame.mixer.init()

CORRECT_SOUND = "sounds/correct.mp3"
WRONG_SOUND = "sounds/wrong.mp3"

class QuizGUI:
    def __init__(self, mobile):
        self.mobile = mobile
        self.root = tk.Tk()
        self.root.title("🧠 Quiz Game")
        self.root.geometry("600x400")
        self.score = 0
        self.category = ""
        self.questions = []
        self.current_q = 0
        self.timer = 15
        self.timer_running = False
        self.selected_option = tk.StringVar()
        self.build_category_ui()

    def build_category_ui(self):
        tk.Label(self.root, text="📚 Select Category", font=("Arial", 16)).pack(pady=20)
        categories = ["Sports", "History", "Movies", "General Knowledge", "Science"]

        for cat in categories:
            tk.Button(
                self.root, text=cat, font=("Arial", 14), width=20,
                command=lambda c=cat: self.load_questions(c)
            ).pack(pady=5)

    def load_questions(self, cat):
        self.category = cat
        res = requests.get(f"http://127.0.0.1:5001/api/questions?category={cat}")
        if res.status_code == 200:
            self.questions = res.json()
            self.build_quiz_ui()
        else:
            messagebox.showerror("Error", "Failed to load questions")

    def build_quiz_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.q_label = tk.Label(self.root, text="", font=("Arial", 14), wraplength=500)
        self.q_label.pack(pady=20)

        self.options = []
        for _ in range(4):
            btn = tk.Radiobutton(
                self.root, variable=self.selected_option, value="", text="", 
                font=("Arial", 12), indicatoron=0, width=40, pady=5,
                command=self.check_answer
            )
            btn.pack(pady=5)
            self.options.append(btn)

        self.timer_label = tk.Label(self.root, text="⏱️ Time left: 15", font=("Arial", 12), fg="red")
        self.timer_label.pack(pady=10)

        self.load_question()

    def load_question(self):
        if self.current_q >= len(self.questions):
            self.finish_quiz()
            return

        q_data = self.questions[self.current_q]
        self.selected_option.set(None)
        self.q_label.config(text=f"Q{self.current_q + 1}: {q_data['question']}")

        for i, opt in enumerate(q_data['options']):
            self.options[i].config(text=opt, value=str(i+1))  # value is option index

        self.timer = 15
        self.update_timer()
        self.timer_running = True
        threading.Thread(target=self.run_timer, daemon=True).start()

    def run_timer(self):
        while self.timer > 0 and self.timer_running:
            time.sleep(1)
            self.timer -= 1
            self.update_timer()
        if self.timer == 0 and self.timer_running:
            self.timer_running = False
            self.auto_next()

    def update_timer(self):
        self.timer_label.config(text=f"⏱️ Time left: {self.timer}")

    def check_answer(self):
        self.timer_running = False
        selected = self.selected_option.get()
        correct = str(self.questions[self.current_q]["answer"])  # numeric index as string

        if selected == correct:
            self.score += 1
            pygame.mixer.music.load(CORRECT_SOUND)
        else:
            pygame.mixer.music.load(WRONG_SOUND)

        pygame.mixer.music.play()
        self.root.after(1000, self.next_question)

    def auto_next(self):
        pygame.mixer.music.load(WRONG_SOUND)
        pygame.mixer.music.play()
        self.root.after(1000, self.next_question)

    def next_question(self):
        self.current_q += 1
        self.load_question()

    def finish_quiz(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="🎉 Quiz Over!", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text=f"Your Score: {self.score}/{len(self.questions)}", font=("Arial", 16)).pack(pady=10)

        # Submit score to backend
        requests.post("http://127.0.0.1:5001/submit_score", json={
            "mobile": self.mobile,
            "category": self.category,
            "score": self.score
        })

        tk.Button(self.root, text="Exit", font=("Arial", 14), command=self.root.destroy).pack(pady=20)

def start_quiz(mobile):
    app = QuizGUI(mobile)
    app.root.mainloop()
