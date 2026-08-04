import tkinter as tk
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    current_words = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    word_dict = original_data.to_dict(orient="records")
else:
    word_dict = current_words.to_dict(orient="records")

current_card = {}
flip_timer = None


def next_card():
    global current_card, flip_timer
    if flip_timer:
        window.after_cancel(flip_timer)

    current_card = random.choice(word_dict)

    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)

    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    word_dict.remove(current_card)
    updated_data = pd.DataFrame(word_dict)
    updated_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def dont_know():
    next_card()


window = tk.Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_front_img = tk.PhotoImage(file="images/card_front.png")
card_back_img = tk.PhotoImage(file="images/card_back.png")

canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_image = tk.PhotoImage(file="images/right.png")
know_button = tk.Button(image=right_image, highlightthickness=0, command=is_known)
know_button.grid(row=1, column=1)

wrong_image = tk.PhotoImage(file="images/wrong.png")
unknown_button = tk.Button(image=wrong_image, highlightthickness=0, command=dont_know)
unknown_button.grid(row=1, column=0)

next_card()

window.mainloop()