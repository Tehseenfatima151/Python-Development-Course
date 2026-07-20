# Day 12 – Global vs Local Scope, Namespace & Number Guessing Game

## 📌 Overview
Is session mein humne **variable scope** ka detailed concept seekha — global aur local scope mein farq, **namespace** ka matlab, `global` keyword ka use, aur Python ka **LEGB rule**. Iske baad humne ye concepts practically apply kar ke ek **Number Guessing Game** banaya.

---

## 1️⃣ What is Scope?

**Scope** batata hai ke koi variable program ke kis hisse mein accessible (use ho sakta) hai. Python mein do main types ki scope hoti hain:

- **Global Scope** – Variable jo function ke bahar define hota hai, poore program mein accessible hota hai
- **Local Scope** – Variable jo function ke andar define hota hai, sirf usi function ke andar accessible hota hai

---

## 2️⃣ Local Scope

Function ke andar banaya gaya variable sirf **usi function tak mehdood** hota hai — bahar se access nahi ho sakta.

```python
def my_function():
    local_var = "I am local"
    print(local_var)

my_function()          # Output: I am local
print(local_var)       # NameError: name 'local_var' is not defined
```

Jaise hi function ka execution khatam hota hai, uske local variables **memory se delete** ho jate hain.

---

## 3️⃣ Global Scope

Function ke bahar (program ke top level pe) banaya gaya variable **global** hota hai — poore program mein, functions ke andar bhi, accessible hota hai (read karne ke liye).

```python
global_var = "I am global"

def my_function():
    print(global_var)   # Function ke andar se global variable read kar sakte hain

my_function()            # Output: I am global
print(global_var)        # Output: I am global
```

---

## 4️⃣ Local Variable Global Variable ko "Shadow" Karta Hai

Agar function ke andar **same naam** ka variable define ho, to Python usse local samjhega — asal global variable change nahi hoga.

```python
enemies = 1

def increase_enemies():
    enemies = 2         # Ye ek naya LOCAL variable hai, global wala nahi change ho raha
    print(f"enemies inside function: {enemies}")

increase_enemies()       # Output: enemies inside function: 2
print(f"enemies outside function: {enemies}")   # Output: enemies outside function: 1
```

Ye ek common confusion hai — function ke andar `enemies = 2` likhne se global `enemies` update nahi hota, balke ek naya local `enemies` ban jata hai jo sirf function ke andar exist karta hai.

---

## 5️⃣ `global` Keyword — Global Variable ko Function ke Andar se Modify Karna

Agar hum chahte hain ke function ke andar se **asal global variable** modify ho, to `global` keyword use karte hain.

```python
enemies = 1

def increase_enemies():
    global enemies       # Batata hai ke ye local nahi, global variable hai
    enemies += 1
    print(f"enemies inside function: {enemies}")

increase_enemies()       # Output: enemies inside function: 2
print(f"enemies outside function: {enemies}")   # Output: enemies outside function: 2
```

⚠️ **Best Practice:** `global` keyword ka zyada use karna generally acha practice nahi mana jata, kyunke isse code samajhna mushkil ho jata hai aur bugs aa sakte hain (function kahin se bhi global state change kar sakta hai). Behtar hai ke function `return` use kar ke value wapis bheje.

```python
enemies = 1

def increase_enemies(current_enemies):
    return current_enemies + 1

enemies = increase_enemies(enemies)
print(enemies)   # Output: 2
```

---

## 6️⃣ Python's Built-in Global Scope (Keywords)

Python ke apne built-in functions aur keywords (jaise `print`, `len`, `input`) bhi ek tarah ki **global scope** mein hote hain — hum unhe kahin se bhi call kar sakte hain bina import kiye.

```python
print(len("Hello"))   # len() Python ki built-in global scope se aata hai
```

---

## 7️⃣ Namespace

**Namespace** ek system hai jisse Python track karta hai ke kaunsa naam (variable/function) kis scope mein maujood hai aur uski value kya hai — takay do alag scopes mein same naam ke variables aapas mein clash na karein.

```python
x = "global x"

def outer_function():
    x = "outer x"

    def inner_function():
        x = "inner x"
        print(x)          # inner namespace se

    inner_function()
    print(x)               # outer namespace se

outer_function()
print(x)                    # global namespace se
```

**Output:**
```
inner x
outer x
global x
```

Har function ka apna alag namespace hota hai — is liye same naam ke variables alag alag jagah bina conflict ke exist kar sakte hain.

---

## 8️⃣ LEGB Rule (Scope Resolution Order)

Python jab kisi variable ko dhoondta hai, to is order mein search karta hai:

1. **L – Local** (current function ke andar)
2. **E – Enclosing** (agar function kisi aur function ke andar nested hai)
3. **G – Global** (module/program level)
4. **B – Built-in** (Python ki apni built-in functions/keywords)

```python
x = "global"   # Global

def outer():
    x = "enclosing"   # Enclosing

    def inner():
        x = "local"    # Local
        print(x)        # Pehle Local mein dhoondega -> "local"

    inner()

outer()
```

---

## 9️⃣ Number Guessing Game

**Concept:** Computer aik random number (1-100) choose karta hai, player usse guess karta hai, aur har guess ke baad "too high" ya "too low" ka hint milta hai jab tak sahi number na mil jaye.

### Step 1: Random Number Generate Karna

```python
import random

answer = random.randint(1, 100)
```

### Step 2: Guess Check Karne ka Function

```python
def check_guess(guess, actual_answer, turns):
    """Compares guess to answer and returns remaining turns."""
    if guess > actual_answer:
        print("Too high.")
        return turns - 1
    elif guess < actual_answer:
        print("Too low.")
        return turns - 1
    else:
        print(f"You got it! The answer was {actual_answer}.")
        return turns   # Game khatam, turns waisay hi rehne do
```

### Step 3: Difficulty Level Set Karna

```python
def set_difficulty():
    level = input("Choose a difficulty. Type 'easy' or 'hard': ").lower()
    if level == "easy":
        return 10
    else:
        return 5
```

### Step 4: Main Game Logic

```python
def guess_number():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")

    answer = random.randint(1, 100)
    turns = set_difficulty()
    guess = 0

    while guess != answer:
        if turns == 0:
            print("You've run out of guesses. Game over!")
            return
        else:
            print(f"You have {turns} attempts remaining.")
            guess = int(input("Make a guess: "))
            turns = check_guess(guess, answer, turns)

    print("🎉 Congratulations, you guessed the correct number!")
```

**Explanation:**
- `set_difficulty()` function turns decide karta hai (easy = 10, hard = 5) — is se hum **local scope** ka practical use dekhte hain, kyunke `level` variable sirf usi function tak mehdood hai
- `check_guess()` function har guess ke baad turns update karta hai aur wapis bhejta hai (`return`) — isse global variable modify karne ki zaroorat hi nahi parti
- Main `guess_number()` function `while` loop mein tab tak chalta hai jab tak sahi guess na ho jaye ya turns khatam na ho jayein

---

## 🔟 Full Combined Program

```python
import random

def check_guess(guess, actual_answer, turns):
    """Compares guess to answer and returns remaining turns."""
    if guess > actual_answer:
        print("Too high.")
        return turns - 1
    elif guess < actual_answer:
        print("Too low.")
        return turns - 1
    else:
        print(f"You got it! The answer was {actual_answer}.")
        return turns


def set_difficulty():
    """Asks user for difficulty and returns number of turns."""
    level = input("Choose a difficulty. Type 'easy' or 'hard': ").lower()
    if level == "easy":
        return 10
    else:
        return 5


def guess_number():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")

    answer = random.randint(1, 100)
    turns = set_difficulty()
    guess = 0

    while guess != answer:
        if turns == 0:
            print("You've run out of guesses. Game over!")
            return
        else:
            print(f"You have {turns} attempts remaining.")
            guess = int(input("Make a guess: "))
            turns = check_guess(guess, answer, turns)

    print("🎉 Congratulations, you guessed the correct number!")


guess_number()
```

---

## 1️⃣1️⃣ Example Run

```
Welcome to the Number Guessing Game!
I'm thinking of a number between 1 and 100.
Choose a difficulty. Type 'easy' or 'hard': easy
You have 10 attempts remaining.
Make a guess: 50
Too high.
You have 9 attempts remaining.
Make a guess: 25
Too low.
You have 8 attempts remaining.
Make a guess: 37
You got it! The answer was 37.
🎉 Congratulations, you guessed the correct number!
```

---

## ✅ Key Takeaways
- Local variables sirf function ke andar accessible hote hain, function khatam hote hi delete ho jate hain
- Global variables poore program mein accessible hote hain (read ke liye), lekin function ke andar naya same-naam variable banane se wo sirf local shadow banata hai
- `global` keyword se function ke andar se asal global variable modify kiya ja sakta hai — lekin ye best practice nahi, `return` use karna behtar hai
- Namespace har scope ke variables ko alag track karta hai taake naam clash na ho
- LEGB rule (Local → Enclosing → Global → Built-in) Python ka variable search order hai
- Number Guessing Game mein functions se values return kar ke humne `global` keyword use kiye bina hi state (turns) update ki — ye clean scope management ka acha example hai

---

## 🔗 Practice Task
- Game mein ek "hint" system add karo jo har 3 wrong guesses ke baad range narrow kar de
- `global` keyword use kar ke wahi game dobara likho aur dono approaches compare karo
- Ek function banao jo LEGB rule demonstrate kare — 4 levels ki nested functions ke sath
