# Day 31 – Capstone Project: Flash Card App

## 📌 Overview
Ye ek **capstone project** hai jo pichle kai hafton ke concepts ek sath combine karta hai — Tkinter GUI (Day 27-28), pandas/CSV handling (Day 25-26), aur `after()` timer (Day 28). Humne ek **Flash Card language-learning app** banayi (French-to-English) jo random words show karti hai, "known" words ko permanently list se hata deti hai, aur progress ko CSV mein save karti hai taake next session mein wahi se continue ho.

---

## 1️⃣ Project Structure

```
flashcard_app/
├── main.py
├── data/
│   ├── french_words.csv          (original word list)
│   └── words_to_learn.csv        (auto-generated — sirf unknown words)
└── images/
    ├── card_front.png             (question side)
    ├── card_back.png               (answer side)
    ├── right.png                   (✓ button icon)
    └── wrong.png                    (✗ button icon)
```

---

## 2️⃣ Game Concept

- Ek random French word screen pe show hota hai (card front)
- **3 seconds baad automatically** card flip ho kar English translation dikhata hai (card back)
- Agar word **pata hai** (✓ button) → wo word list se **permanently hata diya jata hai**
- Agar word **pata nahi** (✗ button) → wo list mein rehta hai, dobara aa sakta hai
- Progress `words_to_learn.csv` mein save hota hai — agli baar app khulne pe **wahi se continue** hoti hai jahan chhora tha

---

## 3️⃣ Step 1: Reading Words with Pandas (Day 25-26 Concepts)

```python
import pandas as pd
import random

try:
    current_words = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    word_dict = original_data.to_dict(orient="records")
else:
    word_dict = current_words.to_dict(orient="records")
```

**Explanation:**
- `try-except` — pehli baar app run hone pe `words_to_learn.csv` exist nahi karti, is liye original file (`french_words.csv`) se start karte hain
- Agar `words_to_learn.csv` **pehle se maujood hai** (matlab pehle bhi practice ho chuki hai), to usi se continue karte hain — is se already-known words dobara nahi puchay jate
- `.to_dict(orient="records")` — DataFrame ko list of dictionaries mein convert karta hai, jaise: `[{"French": "le chat", "English": "the cat"}, ...]`

---

## 4️⃣ Step 2: Random Word Generate Karna & Card Front Show Karna

```python
current_card = {}

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    current_card = random.choice(word_dict)

    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)

    flip_timer = window.after(3000, func=flip_card)
```

**Explanation:**
- `random.choice(word_dict)` — list of dictionaries mein se ek random word-dictionary select karta hai
- `window.after_cancel(flip_timer)` — agar previous card ka flip-timer abhi bhi pending hai, to usse cancel karte hain — warna purana timer galat waqt pe naya card flip kar sakta hai
- `flip_timer = window.after(3000, func=flip_card)` — naya 3-second timer set karta hai jo naye card ko automatically flip karega

---

## 5️⃣ Step 3: Card Flip Function

```python
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)
```

**Explanation:** `canvas.itemconfig()` existing canvas elements (background image, text) ko update karta hai — naya element banane ki bajaye jo already hai usse "flip" jaisa effect dete hain.

---

## 6️⃣ Step 4: "Know" Button — Word Ko List Se Hatana

```python
def is_known():
    word_dict.remove(current_card)
    updated_data = pd.DataFrame(word_dict)
    updated_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()
```

**Explanation:**
- `word_dict.remove(current_card)` — current word ko list se permanently remove karta hai
- `pd.DataFrame(word_dict)` — updated (chhoti) list ko wapis DataFrame mein convert karte hain
- `.to_csv(...)` — file mein save kar dete hain, taake progress persist ho — agli baar ye word dobara nahi aayega
- `next_card()` — turant agla random word show karta hai

---

## 7️⃣ Step 5: "Don't Know" Button

```python
def dont_know():
    next_card()
```

**Explanation:** Simple — bas agla random card dikha do, current word list mein hi rehta hai (dobara puchne ke liye).

---

## 8️⃣ Step 6: GUI Layout (Buttons with Images)

```python
right_image = tk.PhotoImage(file="images/right.png")
know_button = tk.Button(image=right_image, highlightthickness=0, command=is_known)
know_button.grid(row=1, column=1)

wrong_image = tk.PhotoImage(file="images/wrong.png")
unknown_button = tk.Button(image=wrong_image, highlightthickness=0, command=dont_know)
unknown_button.grid(row=1, column=0)
```

**Explanation:**
- `tk.Button(image=..., command=...)` — text ki bajaye image-based buttons — GUI ko zyada visually appealing banate hain
- `highlightthickness=0` — button ke around default border/outline hata deta hai
- Bilkul Day 27-28 wala callback pattern — `command=is_known` (bina brackets ke)

---

## 9️⃣ Full Combined `main.py`

```python
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
```

---

## 📸 Screenshot


<img width="1159" height="721" alt="1" src="https://github.com/user-attachments/assets/96c65dd1-4c6b-4b61-adc3-bdfb3f62204a" />

---

## ✅ Key Takeaways
- Ye capstone project 3 alag skill-sets combine karta hai: **pandas (data)**, **Tkinter (GUI)**, aur **after() timers (automation)**
- `try-except FileNotFoundError` se app ko "resume from last session" behavior milta hai — pehli run vs baad ki runs ko gracefully handle karta hai
- `word_dict.remove()` + `to_csv()` pattern se **persistent learning progress** banaya — user ka data sessions ke beech safe rehta hai
- Timer cancel karna (`after_cancel`) zaroori hai jab user manually next card pe jaye, warna purana pending timer conflict create karta hai
- Image-based buttons (`tk.Button(image=...)`) GUI ko professional aur polished look dete hain
- `canvas.itemconfig()` — existing elements ko update karna, naye create karne se zyada efficient aur clean approach hai

---

## 🔗 Practice Task
- Ek score counter add karo jo session ke dauran "known" vs "unknown" count track kare
- Language selection add karo (French ke ilawa Spanish/German bhi option ho, alag CSV files se)
- Jab sare words "known" ho jayein, ek "Congratulations! You've learned all words" message show karo
