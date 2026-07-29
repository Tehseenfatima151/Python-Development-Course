# Day 17 – Creating Your Own Classes & Quiz Game

## 📌 Overview
Is session mein humne **apni khud ki classes** banana seekha — attributes kaise define karte hain, **constructor (`__init__`)** ka role kya hota hai, aur multiple classes ko aapas mein kaise interact karwate hain. Iske baad humne ye concepts use kar ke ek complete **Quiz Game** banaya jo true/false trivia questions puchta hai aur score track karta hai.

---

## 1️⃣ Creating Your Own Class (Recap + Detail)

Class banane ka basic structure:

```python
class ClassName:
    def __init__(self, parameter1, parameter2):
        self.attribute1 = parameter1
        self.attribute2 = parameter2
```

**Example — A simple `User` class:**

```python
class User:
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
        self.followers = 0
        self.following = 0

    def follow(self, other_user):
        other_user.followers += 1
        self.following += 1


user_1 = User("001", "Ali")
user_2 = User("002", "Sara")

user_1.follow(user_2)
print(user_1.following)    # Output: 1
print(user_2.followers)    # Output: 1
```

---

## 2️⃣ Attributes in Detail

**Attributes** class ke andar store hone wala data hai — har object apni khud ki attribute values rakhta hai.

```python
class Car:
    def __init__(self, model, year):
        self.model = model
        self.year = year

car_1 = Car("Corolla", 2022)
car_2 = Car("Civic", 2023)

print(car_1.model)   # Output: Corolla
print(car_2.model)   # Output: Civic
```

Notice: `car_1` aur `car_2` alag alag objects hain, dono ke `model` attribute ki values bhi alag hain — **har object apna independent data rakhta hai**.

### Default Attributes

Kuch attributes hum constructor se pass hone ki bajaye khud se default value de dete hain:

```python
class Car:
    def __init__(self, model, year):
        self.model = model
        self.year = year
        self.speed = 0        # Default value, koi bhi naya car 0 speed pe start hoga
        self.is_running = False
```

---

## 3️⃣ The Constructor (`__init__`) — Detail

`__init__()` ek **special method** hai jo har naye object ke banate hi **automatically** call ho jati hai. Iska kaam hai object ko initial values set karna.

```python
class Book:
    def __init__(self, title, author, pages):
        print(f"Creating a new book: {title}")
        self.title = title
        self.author = author
        self.pages = pages


book_1 = Book("Python Basics", "Ali Khan", 250)
# Output turant print hoga: Creating a new book: Python Basics
```

**Important points about `__init__`:**
- Naam humesha `__init__` hi hota hai (double underscore dono taraf)
- Automatically call hota hai — humein khud se call nahi karna parta
- `self` pehla parameter hota hai (current object ko refer karta hai)
- Yahan hum jitne bhi attributes set karte hain, wo poori class mein `self.attribute_name` se access hote hain

---

## 4️⃣ Methods that Use Attributes

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calculate_area(self):
        return self.width * self.height

    def calculate_perimeter(self):
        return 2 * (self.width + self.height)


rect = Rectangle(5, 3)
print(rect.calculate_area())        # Output: 15
print(rect.calculate_perimeter())   # Output: 16
```

**Explanation:** Method ke andar `self.width` aur `self.height` use kar ke hum **usi object ki** values access karte hain — is se method dynamically kaam karta hai chahe kitne bhi Rectangle objects ban jayein.

---

## 5️⃣ Building the Quiz Game

Quiz Game ko humne **2 classes** mein organize kiya:

| Class | Responsibility |
|-------|-----------------|
| `Question` | Ek single question ka text aur uska sahi answer store karta hai |
| `QuizBrain` | Poore quiz ko chalata hai — score track karta hai, agla question deta hai, answer check karta hai |

### Step 1: `Question` Class

```python
class Question:
    """Models a single True/False question with its text and correct answer."""

    def __init__(self, text, answer):
        self.text = text
        self.answer = answer
```

### Step 2: Question Data (List of Question Objects)

```python
question_data = [
    {"text": "A slug's blood is green.", "answer": "True"},
    {"text": "The Great Wall of China is visible from space.", "answer": "False"},
    {"text": "In 1386 a French court sentenced a pig to death for murder.", "answer": "True"},
    {"text": "A shrimp's heart is in its head.", "answer": "True"},
    {"text": "Google was originally called Backrub.", "answer": "True"},
    {"text": "Python was named after the programming language.", "answer": "False"},
]

question_bank = []
for question in question_data:
    new_question = Question(question["text"], question["answer"])
    question_bank.append(new_question)
```

**Explanation:** Har dictionary se ek `Question` object banaya ja raha hai aur `question_bank` list mein add ho raha hai — ye "list of objects" pattern hai (jaisa Day 9/14 mein "list of dictionaries" dekha tha, bas ab dictionaries ki jagah custom objects hain).

### Step 3: `QuizBrain` Class

```python
class QuizBrain:
    """Handles quiz logic: tracking progress, asking questions, checking answers."""

    def __init__(self, question_list):
        self.question_number = 0
        self.score = 0
        self.question_list = question_list

    def still_has_questions(self):
        """Returns True if there are more questions left in the quiz."""
        return self.question_number < len(self.question_list)

    def next_question(self):
        """Displays the next question and checks the user's answer."""
        current_question = self.question_list[self.question_number]
        self.question_number += 1

        user_answer = input(f"Q.{self.question_number}: {current_question.text} (True/False): ")
        self.check_answer(user_answer, current_question.answer)

    def check_answer(self, user_answer, correct_answer):
        """Compares user's answer with the correct answer and updates the score."""
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            print("You got it right!")
        else:
            print("That's wrong.")

        print(f"The correct answer was: {correct_answer}")
        print(f"Your current score is: {self.score}/{self.question_number}\n")
```

**Explanation:**
- `question_number` aur `score` **quiz ki state** hain — ye QuizBrain ke andar encapsulated hain
- `still_has_questions()` batata hai ke quiz khatam hua ya nahi
- `next_question()` current question show karta hai, user se input leta hai, aur check karwata hai
- `check_answer()` sahi/galat verify kar ke score update karta hai

---

## 6️⃣ Main Program (Running the Quiz)

```python
quiz = QuizBrain(question_bank)

while quiz.still_has_questions():
    quiz.next_question()

print("You've completed the quiz!")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")
```

---

## 7️⃣ Full Combined Program

```python
class Question:
    """Models a single True/False question with its text and correct answer."""

    def __init__(self, text, answer):
        self.text = text
        self.answer = answer


class QuizBrain:
    """Handles quiz logic: tracking progress, asking questions, checking answers."""

    def __init__(self, question_list):
        self.question_number = 0
        self.score = 0
        self.question_list = question_list

    def still_has_questions(self):
        """Returns True if there are more questions left in the quiz."""
        return self.question_number < len(self.question_list)

    def next_question(self):
        """Displays the next question and checks the user's answer."""
        current_question = self.question_list[self.question_number]
        self.question_number += 1

        user_answer = input(f"Q.{self.question_number}: {current_question.text} (True/False): ")
        self.check_answer(user_answer, current_question.answer)

    def check_answer(self, user_answer, correct_answer):
        """Compares user's answer with the correct answer and updates the score."""
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            print("You got it right!")
        else:
            print("That's wrong.")

        print(f"The correct answer was: {correct_answer}")
        print(f"Your current score is: {self.score}/{self.question_number}\n")


question_data = [
    {"text": "A slug's blood is green.", "answer": "True"},
    {"text": "The Great Wall of China is visible from space.", "answer": "False"},
    {"text": "In 1386 a French court sentenced a pig to death for murder.", "answer": "True"},
    {"text": "A shrimp's heart is in its head.", "answer": "True"},
    {"text": "Google was originally called Backrub.", "answer": "True"},
    {"text": "Python was named after the programming language.", "answer": "False"},
]

question_bank = []
for question in question_data:
    new_question = Question(question["text"], question["answer"])
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)

while quiz.still_has_questions():
    quiz.next_question()

print("You've completed the quiz!")
print(f"Your final score was: {quiz.score}/{quiz.question_number}")
```

---

## 8️⃣ Example Run

```
Q.1: A slug's blood is green. (True/False): True
You got it right!
The correct answer was: True
Your current score is: 1/1

Q.2: The Great Wall of China is visible from space. (True/False): True
That's wrong.
The correct answer was: False
Your current score is: 1/2

...

You've completed the quiz!
Your final score was: 4/6
```

---

## 📸 Screenshot

<!-- Terminal output ka screenshot yahan drag & drop karo -->

---

## ✅ Key Takeaways
- Apni khud ki class banane ke liye `class ClassName:` likhte hain aur `__init__` mein attributes set karte hain
- `self` object ke apne data ko refer karta hai — har object independent attributes rakhta hai
- `__init__` constructor hai jo object banate hi automatically chalta hai, koi bhi manual call nahi karni parti
- Methods `self.attribute` use kar ke object ke data ke sath kaam karte hain
- Bare projects ko multiple classes mein todna (jaise `Question` aur `QuizBrain`) responsibilities ko clean separate karta hai
- "List of objects" pattern (dictionaries se custom objects banana) real-world data ko model karne ka professional tareeqa hai

---

## 🔗 Practice Task
- Quiz mein "shuffle questions" feature add karo taake har baar order alag ho
- `Question` class mein ek `category` attribute add karo (jaise Science, History) aur user se category choose karwao
- Quiz khatam hone pe percentage score bhi show karo (e.g. "You scored 66%")
