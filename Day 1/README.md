# Day 1 – Simple Printing, User Input & Concatenation

## 📌 Overview
Ye Python programming ka pehla session tha. Is mein humne seekha ke screen pe output kaise print karte hain, user se input kaise lete hain, aur strings ko aapas mein join (concatenate) kaise karte hain.

---

## 1️⃣ Simple Printing

Python mein screen pe kuch bhi show karne ke liye `print()` function use hota hai.

```python
print("Hello, World!")
print("Welcome to Python Programming Bootcamp")
```

**Multiple values ek print statement mein:**

```python
print("Hello", "Ali", "Welcome")
# Output: Hello Ali Welcome
```

**`print()` automatically har statement ke baad new line add kar deta hai:**

```python
print("Line 1")
print("Line 2")
# Output:
# Line 1
# Line 2
```

**`sep` aur `end` parameters:**

```python
print("Ali", "Ahmed", sep=" - ")
# Output: Ali - Ahmed

print("Hello", end=" ")
print("World")
# Output: Hello World
```

---

## 2️⃣ User Input

User se data lene ke liye `input()` function use hota hai. Ye hamesha **string** ke roop mein value return karta hai.

```python
name = input("Enter your name: ")
print("Hello,", name)
```

**Example with a question:**

```python
city = input("Which city do you live in? ")
print(f"You live in {city}")
```

⚠️ **Important:** `input()` se jo bhi value aayegi wo hamesha `string` type ki hogi, chahe user number hi kyun na likhe.

```python
age = input("Enter your age: ")
print(type(age))   # <class 'str'>
```

Agar number pe calculation karni ho to usse convert karna zaroori hai:

```python
age = int(input("Enter your age: "))
print(age + 1)
```

---

## 3️⃣ Concatenation

Concatenation ka matlab hai do ya zyada strings ko aapas mein jodna (`+` operator use karke).

```python
first_name = "Muhammad"
last_name = "Ali"

full_name = first_name + " " + last_name
print(full_name)
# Output: Muhammad Ali
```

**Concatenation sirf strings ke sath kaam karta hai** — agar number ko string ke sath jodna ho to pehle usse `str()` se convert karna padta hai:

```python
age = 22
message = "I am " + str(age) + " years old"
print(message)
# Output: I am 22 years old
```

❌ **Ye galat hoga (error dega):**
```python
age = 22
print("I am " + age + " years old")
# TypeError: can only concatenate str (not "int") to str
```

---

## ✅ Key Takeaways
- `print()` output show karne ke liye use hota hai, `sep` aur `end` se format control hoti hai
- `input()` hamesha string return karta hai, numbers ke liye convert karna zaroori hai
- Concatenation (`+`) sirf strings ko jodne ke kaam aata hai
- Numbers ko strings ke sath concatenate karne se pehle `str()` use karna zaroori hai

---

## 🔗 Practice Task
- User se uska naam aur city poocho aur aik friendly welcome message print karo
- User se do numbers lo (input se) aur unhe string concatenation se ek sentence mein show karo
- `sep` aur `end` parameters use karke apna naam, father's name aur city ek hi line mein print karo
