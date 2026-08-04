# Day 34 – Trivia API & The Quizzler App (GUI Quiz)

## 📌 Overview
Is session mein humne ek **Trivia API** se live quiz questions fetch karna seekha, aur unhe ek **Tkinter GUI** mein present karne wala poora **Quizzler App** banaya. Ye project Day 17 (Question/QuizBrain classes) ko Day 33 (APIs) aur Day 27-28 (Tkinter) ke sath combine karta hai — is dafa quiz terminal mein nahi, balke ek proper desktop app mein chalta hai, jisme live internet se questions aate hain.

---

## 1️⃣ The Trivia API (Open Trivia Database)

`opentdb.com` ek free, public API hai jo random trivia questions deta hai — categories, difficulty, aur question-type customize kiye ja sakte hain.

```python
import requests

parameters = {
    "amount": 10,
    "type": "boolean",   # True/False questions
}

response = requests.get(url="https://opentdb.com/api.php", params=parameters)
response.raise_for_status()
data = response.json()

question_data = data["results"]
```

**Explanation:**
- `params` se hum batate hain ke kitne (`amount`) aur kaise (`type`) questions chahiye
- Response ka `"results"` key ek list of dictionaries deta hai, har dictionary mein question, correct answer, category, waghera hoti hai

---

## 2️⃣ Handling HTML Entities in API Responses

Trivia API ka text kabhi kabhi **HTML-encoded characters** ke sath aata hai — jaise `&quot;`, `&#039;`, `&amp;`.

```python
import html

raw_text = "It&#039;s a &quot;test&quot;"
clean_text = html.unescape(raw_text)
print(clean_text)   # It's a "test"
```

**Explanation:** `html.unescape()` in encoded characters ko wapis normal readable text mein convert kar deta hai — Trivia API se aane wale har question/answer ko is se clean karna zaroori hai.

---

## 3️⃣ Building the Quizzler App

### Project Structure

```
quizzler_app/
├── main.py
├── data.py           (API se questions fetch karta hai)
├── question_model.py  (Question class)
├── quiz_brain.py       (QuizBrain class)
└── ui.py                 (Tkinter GUI)
```

---

## 4️⃣ `question_model.py` — Question Class

```python
class Question:
    """Models a single trivia question with its text and correct answer."""

    def __init__(self, q_text, q_answer):
        self.text = q_text
        self.answer = q_answer
```

**Explanation:** Bilkul Day 17 wali `Question` class jaisi — bas ab data ek local list ki bajaye live API se aata hai.

---

## 5️⃣ `data.py` — Fetching Questions from the API

```python
import requests
import html

parameters = {
    "amount": 10,
    "type": "boolean",
}

response = requests.get(url="https://opentdb.com/api.php", params=parameters)
response.raise_for_status()
data = response.json()

question_data = data["results"]

for question in question_data:
    question["question"] = html.unescape(question["question"])
```

**Explanation:** Har question ka text loop mein `html.unescape()` se clean kar diya jata hai — is se aage jitni bhi jagah is data ko use karein, wo already clean hoga.

---

## 6️⃣ `quiz_brain.py` — QuizBrain Class (GUI-Aware Version)

```python
import html


class QuizBrain:
    """Handles quiz logic: tracking progress, checking answers, updating score."""

    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number}: {q_text}"

    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False
```

**Explanation:**
- Bilkul Day 17 wale `QuizBrain` jaisa logic, lekin ab `input()` use nahi karta — buttons se milne wala `user_answer` parameter leta hai
- `next_question()` ab question text **return karta hai** (GUI mein display karne ke liye), print nahi karta
- `check_answer()` **True/False return karta hai** (GUI mein color feedback dikhane ke liye)

---

## 7️⃣ `ui.py` — Tkinter GUI (Day 27-28 Concepts)

```python
import tkinter as tk

THEME_COLOR = "#375362"


class QuizInterface:
    """Builds and manages the Tkinter GUI for the quiz."""

    def __init__(self, quiz_brain):
        self.quiz = quiz_brain

        self.window = tk.Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = tk.Label(text="Score: 0", bg=THEME_COLOR, fg="white")
        self.score_label.grid(row=0, column=1)

        self.canvas = tk.Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150, 125, width=280, text="Some Question Text",
            fill=THEME_COLOR, font=("Arial", 20, "italic")
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        true_image = tk.PhotoImage(file="images/true.png")
        self.true_button = tk.Button(image=true_image, highlightthickness=0, command=self.true_pressed)
        self.true_button.grid(row=2, column=0)

        false_image = tk.PhotoImage(file="images/false.png")
        self.false_button = tk.Button(image=false_image, highlightthickness=0, command=self.false_pressed)
        self.false_button.grid(row=2, column=1)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        """Fetches and displays the next question, or ends the quiz."""
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz!")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right):
        """Flashes the canvas green/red depending on the answer, then loads the next question."""
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")

        self.score_label.config(text=f"Score: {self.quiz.score}")
        self.window.after(1000, self.get_next_question)
```

**Explanation:**
- `command=self.true_pressed` — button click pe class ka apna method call hota hai (bilkul Day 27 wala callback pattern, bas ab class method hai)
- `give_feedback()` — canvas ka background color badal deta hai (green = sahi, red = galat) — visual feedback ke liye
- `self.window.after(1000, self.get_next_question)` — 1 second wait kar ke agla question load karta hai (Day 28 wala `after()` concept)

---

## 8️⃣ `main.py` — Bringing It All Together

```python
from data import question_data
from question_model import Question
from quiz_brain import QuizBrain
from ui import QuizInterface

question_bank = []
for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)

print("You've completed the quiz!")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")
```

**Explanation:** `main.py` bohot chota hai — sirf data fetch karta hai, `Question` objects banata hai, `QuizBrain` ko de deta hai, aur `QuizInterface` ko launch kar deta hai. Ye **separation of concerns** ka perfect example hai — har file ki apni ek clear responsibility hai.
## Screenshoot
<img width="960" height="723" alt="1" src="https://github.com/user-attachments/assets/ee06a1bc-0f50-45a7-b6b7-70b1f9d5f141" />

---

## ✅ Key Takeaways
- Trivia API se live, kabhi-na-khatam-hone-wale quiz questions milte hain — hardcoded data se zyada dynamic
- `html.unescape()` API se aane wale HTML-encoded text ko clean karne ke liye zaroori hai
- Same `QuizBrain` logic (Day 17) GUI mein bhi reuse ho sakta hai, bas `input()`/`print()` ki jagah return values aur GUI updates use karte hain — ye acha code reuse dikhata hai
- Canvas background color change karna instant visual feedback dene ka simple, effective tareeqa hai
- Poora project 5 files mein professionally split hai — data fetching, model, logic, aur UI sab alag, jaisa real-world software architecture hota hai

---

## 🔗 Practice Task
- User se category/difficulty choose karwao before quiz start hone (dropdown menu se)
- Quiz khatam hone pe percentage score bhi show karo
- "Play Again" button add karo jo naye questions ke sath quiz restart kare
