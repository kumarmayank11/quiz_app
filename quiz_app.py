import tkinter as tk
from tkinter import messagebox
import json
import random
import os

# Load Questions from JSON
def load_questions():
    with open("questions.json", "r") as file:
        data = json.load(file)
    random.shuffle(data)
    return data

# Save high score
def save_high_score(score):
    try:
        with open("highscore.txt", "r") as f:
            high_score = int(f.read().strip())
    except:
        high_score = 0

    if score > high_score:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
        return score, True
    return high_score, False

# Initialize data
questions = load_questions()
current_index = 0
score = 0

# GUI Functions
def load_next_question():
    global current_index
    if current_index < len(questions):
        q = questions[current_index]
        question_label.config(text=f"Q{current_index+1}: {q['question']}")
        for i in range(4):
            option_buttons[i].config(text=q['options'][i])
    else:
        finish_quiz()

def check_answer(selected):
    global score, current_index
    correct_answer = questions[current_index]["answer"]
    if selected == correct_answer:
        score += 1
    current_index += 1
    load_next_question()

def finish_quiz():
    high, new_record = save_high_score(score)
    msg = f"Your Score: {score}/{len(questions)}\n"
    msg += f"High Score: {high}\n"
    msg += "🎉 New High Score!" if new_record else ""
    messagebox.showinfo("Quiz Completed", msg)
    root.destroy()

# Setup GUI
root = tk.Tk()
root.title("Quiz App")
root.geometry("500x400")

question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=450, justify="left")
question_label.pack(pady=20)

option_buttons = []
for i in range(4):
    btn = tk.Button(root, text="", font=("Arial", 12), width=30, command=lambda i=i: check_answer(option_buttons[i].cget("text")))
    btn.pack(pady=5)
    option_buttons.append(btn)

load_next_question()
root.mainloop()
