# Day 5 – For Loops

## 📌 Overview
Is session mein humne **for loop** ke bunyadi concept ko detail mein seekha — ye kaise kaam karta hai, `range()` function ke sath kaise use hota hai, lists aur strings pe kaise loop chalate hain, aur nested loops kya hote hain. Aakhir mein humne practical projects banaye jisme loops ka real use dekha.

---

## 1️⃣ For Loop Basics

`for` loop kisi bhi sequence (list, string, range, etc.) ke har element pe **baar baar** ek jaisa code chalane ke liye use hota hai. Isse humein manually har item ke liye alag se code likhne ki zaroorat nahi parti.

```python
fruits = ["apple", "banana", "mango"]

for fruit in fruits:
    print(fruit)

# Output:
# apple
# banana
# mango
```

Yahan `fruit` ek temporary variable hai jo har iteration (dohrao) mein list ke agle element ki value le leta hai.

---

## 2️⃣ Looping with `range()`

`range()` function numbers ki ek sequence generate karta hai jisse hum specific number of times loop chala sakte hain.

### `range(stop)` — 0 se start, stop tak (stop exclude hota hai)

```python
for i in range(5):
    print(i)

# Output: 0 1 2 3 4
```

### `range(start, stop)` — start se stop tak

```python
for i in range(2, 6):
    print(i)

# Output: 2 3 4 5
```

### `range(start, stop, step)` — step ke hisaab se number skip karna

```python
for i in range(0, 10, 2):
    print(i)

# Output: 0 2 4 6 8
```

```python
for i in range(10, 0, -1):
    print(i)

# Output: 10 9 8 7 6 5 4 3 2 1  (reverse counting)
```

---

## 3️⃣ Looping through Strings

String bhi ek sequence hoti hai, is liye uspe bhi `for` loop chal sakta hai — har character alag se milta hai.

```python
word = "Python"

for letter in word:
    print(letter)

# Output:
# P
# y
# t
# h
# o
# n
```

---

## 4️⃣ Looping through Lists with Index

Agar element ke sath uska index bhi chahiye ho to `enumerate()` use karte hain.

```python
fruits = ["apple", "banana", "mango"]

for index, fruit in enumerate(fruits):
    print(index, fruit)

# Output:
# 0 apple
# 1 banana
# 2 mango
```

---

## 5️⃣ Nested For Loops (Loop ke andar Loop)

```python
for i in range(1, 4):
    for j in range(1, 3):
        print(f"i={i}, j={j}")

# Output:
# i=1, j=1
# i=1, j=2
# i=2, j=1
# i=2, j=2
# i=3, j=1
# i=3, j=2
```

Nested loops tab useful hote hain jab hume 2D data (jaise matrix ya grid) pe kaam karna ho.

---

## 6️⃣ Loop Control Statements

### `break` — Loop ko beech mein rok dena

```python
for num in range(1, 10):
    if num == 5:
        break
    print(num)

# Output: 1 2 3 4  (5 pe pohanchte hi loop ruk jata hai)
```

### `continue` — Current iteration skip kar ke agli pe chale jana

```python
for num in range(1, 6):
    if num == 3:
        continue
    print(num)

# Output: 1 2 4 5  (3 skip ho jata hai)
```

---

## 7️⃣ Using Loops for Calculations

```python
numbers = [4, 8, 15, 16, 23, 42]
total = 0

for num in numbers:
    total += num   # total = total + num

print(f"Sum: {total}")   # Sum: 108
```

---

## 8️⃣ Practice Projects

### 🔐 Project 1: Random Password Generator (using for loop)

```python
import random
import string

length = int(input("How long should the password be? "))
characters = string.ascii_letters + string.digits + string.punctuation

password = ""
for i in range(length):
    password += random.choice(characters)

print(f"Your generated password is: {password}")
```

**Explanation:** For loop `length` number ki dafa chalta hai, aur har baar `characters` mein se ek random character choose kar ke `password` string mein add karta jata hai.

---

### 🎯 Project 2: FizzBuzz Game

FizzBuzz ek classic programming challenge hai jisme:
- Agar number **3** se divide ho jaye → `"Fizz"` print karo
- Agar number **5** se divide ho jaye → `"Buzz"` print karo
- Agar number **3 aur 5 dono** se divide ho jaye → `"FizzBuzz"` print karo
- Warna number khud print karo

```python
for number in range(1, 101):
    if number % 3 == 0 and number % 5 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print("Buzz")
    else:
        print(number)
```

**Explanation:**
- `%` (modulus) operator remainder check karta hai
- Loop 1 se 100 tak chalta hai
- Sabse pehle `and` wali condition check hoti hai (dono se divisible), phir individually `3` aur `5`
- Order important hai — agar `Fizz`/`Buzz` pehle check karte to `FizzBuzz` kabhi print hi nahi hota

---

## ✅ Key Takeaways
- `for` loop kisi sequence (list, string, range) ke har element pe code repeat karta hai
- `range(start, stop, step)` se number sequences generate hoti hain
- `enumerate()` se index aur value dono ek sath milte hain
- `break` loop ko rok deta hai, `continue` current iteration skip kar deta hai
- Nested loops 2D data ya combinations ke liye use hote hain
- FizzBuzz jaisa challenge loops + conditionals + modulus operator ka combination samjhne ke liye best practice hai

---

## 🔗 Practice Task
- 1 se 50 tak sirf even numbers print karo `for` loop aur `range()` step use kar ke
- Password generator ko modify karo taake wo kam se kam 1 number aur 1 special character guarantee kare
- FizzBuzz ko modify karo — number 7 se divisible ho to `"Bang"` print kare
