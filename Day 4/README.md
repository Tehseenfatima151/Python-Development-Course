# Day 4 – Randomization & Lists

## 📌 Overview
Is session mein humne seekha ke Python mein random values kaise generate karte hain `random` module ki madad se, aur lists kya hoti hain — unhe kaise banate, access karte, aur modify karte hain. Aakhir mein humne kuch practical mini-games bhi banaye jisme randomization aur lists dono concepts use huay.

---

## 1️⃣ Lists

List Python ka aik data type hai jo multiple values ko **ordered** aur **changeable** collection ki soorat mein store karta hai. Square brackets `[]` mein likhi jati hai.

```python
fruits = ["apple", "banana", "mango", "orange"]
print(fruits)
# Output: ['apple', 'banana', 'mango', 'orange']
```

Lists mein different data types bhi ek sath rakh sakte hain:

```python
mixed_list = ["Ali", 22, True, 5.5]
```

### Indexing (List ke elements access karna)

Python mein indexing **0** se start hoti hai.

```python
fruits = ["apple", "banana", "mango", "orange"]

print(fruits[0])    # apple  (first element)
print(fruits[2])    # mango
print(fruits[-1])   # orange (last element, negative indexing)
print(fruits[-2])   # mango  (second last)
```

### Slicing (List ka portion nikalna)

```python
numbers = [10, 20, 30, 40, 50]

print(numbers[1:4])   # [20, 30, 40] -> index 1 se 3 tak
print(numbers[:3])    # [10, 20, 30] -> start se index 2 tak
print(numbers[2:])    # [30, 40, 50] -> index 2 se end tak
```

### Modifying a List

```python
fruits = ["apple", "banana", "mango"]

fruits[1] = "grapes"     # Update element
print(fruits)             # ['apple', 'grapes', 'mango']

fruits.append("orange")   # End mein add karna
print(fruits)             # ['apple', 'grapes', 'mango', 'orange']

fruits.remove("apple")    # Specific element remove karna
print(fruits)             # ['grapes', 'mango', 'orange']

fruits.insert(1, "kiwi")  # Specific index pe insert karna
print(fruits)             # ['grapes', 'kiwi', 'mango', 'orange']
```

### Useful List Functions

```python
numbers = [5, 3, 8, 1, 9]

print(len(numbers))     # List ki length -> 5
print(max(numbers))     # Sabse bara number -> 9
print(min(numbers))     # Sabse chota number -> 1
print(sum(numbers))     # Sab ka sum -> 26

numbers.sort()           # Ascending order
print(numbers)           # [1, 3, 5, 8, 9]

numbers.reverse()        # List ko ulta karna
print(numbers)           # [9, 8, 5, 3, 1]
```

### Nested Lists (List ke andar list)

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(matrix[0])       # [1, 2, 3]
print(matrix[1][2])    # 6 (2nd row, 3rd element)
```

---

## 2️⃣ Randomization

Python mein random values generate karne ke liye `random` module use hota hai. Sabse pehle usse import karna zaroori hai.

```python
import random
```

### `random.randint()` — Random whole number generate karna

```python
import random

num = random.randint(1, 10)
print(num)   # 1 se 10 ke darmiyan koi bhi number (dono inclusive)
```

### `random.choice()` — List se random element choose karna

```python
import random

colors = ["red", "blue", "green", "yellow"]
picked = random.choice(colors)
print(picked)   # List mein se koi bhi ek random color
```

### `random.shuffle()` — List ko shuffle (mix) karna

```python
import random

cards = ["A", "K", "Q", "J", "10"]
random.shuffle(cards)
print(cards)   # Order har dafa alag hoga
```

### `random.random()` — 0 aur 1 ke darmiyan decimal number

```python
import random

print(random.random())   # e.g. 0.6721...
```

---

## 3️⃣ Practice Projects

### 🎮 Project 1: Rock, Paper, Scissors Game

```python
import random

options = ["rock", "paper", "scissors"]

user_choice = input("Choose rock, paper, or scissors: ").lower()
computer_choice = random.choice(options)

print(f"Computer chose: {computer_choice}")

if user_choice == computer_choice:
    print("It's a tie!")
elif user_choice == "rock" and computer_choice == "scissors":
    print("You win! Rock beats Scissors")
elif user_choice == "paper" and computer_choice == "rock":
    print("You win! Paper beats Rock")
elif user_choice == "scissors" and computer_choice == "paper":
    print("You win! Scissors beat Paper")
else:
    print("You lose! Computer wins.")
```

---

### 🗺️ Project 2: Treasure Island Map Game

```python
print("Welcome to Treasure Island!")
print("Your mission is to find the treasure.")

choice1 = input('You are at a crossroad. Go "left" or "right"? ').lower()

if choice1 == "left":
    choice2 = input('You reached a lake. Do you "swim" or "wait"? ').lower()

    if choice2 == "wait":
        choice3 = input('You arrived at an island with three doors. Choose "red", "yellow", or "blue"? ').lower()

        if choice3 == "yellow":
            print("You found the treasure! You win! 🏆")
        elif choice3 == "red":
            print("You got burned by fire. Game Over 🔥")
        else:
            print("You got eaten by a monster. Game Over 👹")
    else:
        print("You got attacked by trout. Game Over 🐟")
else:
    print("You fell into a hole. Game Over 🕳️")
```

---

### 💰 Project 3: Random Person Pays the Bill

```python
import random

people = ["Ali", "Sara", "Ahmed", "Zara", "Bilal"]

print("Friends at the dinner:", people)

lucky_person = random.choice(people)
print(f"{lucky_person} is going to pay the bill today! 💸")
```

---

### 🎲 Project 4: Dice Rolling Simulator

```python
import random

dice_1 = random.randint(1, 6)
dice_2 = random.randint(1, 6)

print(f"You rolled: {dice_1} and {dice_2}")
print(f"Total: {dice_1 + dice_2}")
```

---

### 🔐 Project 5: Random Password Generator

```python
import random
import string

length = int(input("How long should the password be? "))

characters = string.ascii_letters + string.digits + string.punctuation
password = ""

for i in range(length):
    password += random.choice(characters)

print(f"Your generated password: {password}")
```

---

## ✅ Key Takeaways
- Lists ordered, changeable collections hain jo `[]` mein likhi jati hain
- Indexing 0 se start hoti hai, negative indexing end se start hoti hai
- `append()`, `remove()`, `insert()`, `sort()` common list operations hain
- `random` module import karke random numbers, choices, aur shuffling ki jati hai
- `random.randint()` number range ke liye, `random.choice()` list se pick karne ke liye use hota hai
- Real games (Rock Paper Scissors, Treasure Island) mein lists + randomization + control flow sab mil kar use hote hain

---

## 🔗 Practice Task
- Apni khud ki 5-item grocery list banao, usme se 2 items remove karo aur 2 naye add karo
- Rock Paper Scissors game ko modify karo taake best-of-3 rounds ho
- Treasure Island game mein apna khud ka naya path/ending add karo
