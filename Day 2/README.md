## Python Development Pro Bootcamp

# Day 2 – Variables, Data Types, Type Conversion, Number Operations & F-Strings

## 📌 Overview
Is session mein humne Python ke bunyadi building blocks seekhay — variables kaise banate hain, data types kya hote hain, aik type se doosri type mein convert kaise karte hain, numbers pe operations kaise perform karte hain, aur f-strings ka use karke strings ko format kaise karte hain.

---

## 1️⃣ Variables

Variable aik container hota hai jo data ko store karta hai. Python mein variable declare karne ke liye kisi data type ka explicitly likhna zaroori nahi hota (dynamically typed language).

```python
name = "Ali"
age = 22
city = "Lahore"
```

**Rules for naming variables:**
- Variable ka naam letter ya underscore (`_`) se start hona chahiye
- Numbers se start nahi ho sakta (e.g. `2age` invalid hai)
- Spaces allowed nahi (underscore use karo, e.g. `first_name`)
- Case-sensitive hota hai (`Name` aur `name` alag hain)
- Python ke reserved keywords (jaise `class`, `for`, `if`) use nahi kar sakte

---

## 2️⃣ Data Types

Python mein commonly used data types:

| Data Type | Example | Description |
|-----------|---------|-------------|
| `int` | `age = 22` | Whole numbers |
| `float` | `price = 99.99` | Decimal numbers |
| `str` | `name = "Ali"` | Text / strings |
| `bool` | `is_active = True` | True / False values |
| `list` | `fruits = ["apple", "banana"]` | Ordered, changeable collection |
| `tuple` | `point = (2, 3)` | Ordered, unchangeable collection |
| `dict` | `person = {"name": "Ali"}` | Key-value pairs |

Data type check karne ke liye `type()` function use karte hain:

```python
x = 10
print(type(x))   # <class 'int'>
```

---

## 3️⃣ Type Conversion

Aik data type ko doosri type mein convert karna **type conversion** kehlata hai.

### Implicit Conversion
Python khud automatically convert kar deta hai (jab koi data loss na ho):

```python
x = 5        # int
y = 2.0      # float
z = x + y    # Python automatically int ko float bana deta hai
print(z)     # 7.0
```

### Explicit Conversion (Type Casting)
Hum khud function use karke convert karte hain:

```python
a = "10"
b = int(a)      # string se int
print(b + 5)    # 15

c = 3.9
d = int(c)      # float se int (decimal cut ho jata hai)
print(d)        # 3

e = 100
f = str(e)      # int se string
print(f)        # "100"
```

**Common conversion functions:** `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`

---

## 4️⃣ Number Operations

Python mein numbers pe basic arithmetic operations:

```python
a = 10
b = 3

print(a + b)    # Addition       -> 13
print(a - b)    # Subtraction    -> 7
print(a * b)    # Multiplication -> 30
print(a / b)    # Division       -> 3.333...
print(a // b)   # Floor Division -> 3
print(a % b)    # Modulus (remainder) -> 1
print(a ** b)   # Exponent (power) -> 1000
```

**Useful built-in functions:**
```python
print(abs(-5))       # Absolute value -> 5
print(round(3.567, 2))  # Rounding -> 3.57
print(max(4, 9, 2))   # Maximum -> 9
print(min(4, 9, 2))   # Minimum -> 2
```

---

## 5️⃣ F-Strings (Formatted Strings)

F-strings variables ko string ke andar directly insert karne ka modern aur easy tareeqa hai. `f` prefix use hota hai aur variables `{}` curly braces mein likhte hain.

```python
name = "Ali"
age = 22

print(f"My name is {name} and I am {age} years old.")
# Output: My name is Ali and I am 22 years old.
```

**F-strings ke andar expressions bhi likh sakte hain:**

```python
a = 5
b = 3
print(f"Sum of {a} and {b} is {a + b}")
# Output: Sum of 5 and 3 is 8
```

**Number formatting with f-strings:**

```python
price = 49.98765
print(f"Price: {price:.2f}")
# Output: Price: 49.99
```

---

## ✅ Key Takeaways
- Variables Python mein bina explicit type declare kiye ban jate hain
- Har data ka apna type hota hai jo `type()` se check hota hai
- Type conversion implicit (automatic) ya explicit (manual) ho sakti hai
- Arithmetic operators numbers pe calculations ke liye use hote hain
- F-strings string formatting ka sabse readable aur efficient tareeqa hain

---

## 🔗 Practice Task
- Tip Calculator
- Salary bonus calculator
- Shopping discout calculator
