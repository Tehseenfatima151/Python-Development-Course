# Day 3 – Control Flow & Logical Operators

## 📌 Overview
Is session mein humne seekha ke Python mein decisions kaise liye jate hain (if-else statements) aur multiple conditions ko kaise combine karte hain logical operators ki madad se.

---

## 1️⃣ Control Flow (if, elif, else)

Control flow se hum program ko decide karwate hain ke kis condition pe kya code run ho. Ye program ka "decision making" hissa hai.

### Simple `if` Statement

```python
age = 20

if age >= 18:
    print("You are an adult")
```

Agar condition `True` hai to indent wala code run hoga, warna skip ho jayega.

### `if-else` Statement

```python
age = 15

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")
```

### `if-elif-else` Statement (multiple conditions)

```python
marks = 75

if marks >= 90:
    print("Grade: A")
elif marks >= 75:
    print("Grade: B")
elif marks >= 60:
    print("Grade: C")
else:
    print("Grade: F")
```

Python top se neeche conditions check karta hai, jo pehli condition `True` mile usi ka block run hota hai, baqi skip ho jate hain.

### Nested `if` (if ke andar if)

```python
age = 25
has_id = True

if age >= 18:
    if has_id:
        print("Entry allowed")
    else:
        print("ID required")
else:
    print("Entry not allowed")
```

---

## 2️⃣ Comparison Operators (conditions banane ke liye)

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal to | `a == b` |
| `!=` | Not equal to | `a != b` |
| `>` | Greater than | `a > b` |
| `<` | Less than | `a < b` |
| `>=` | Greater than or equal | `a >= b` |
| `<=` | Less than or equal | `a <= b` |

```python
a = 10
b = 5

print(a == b)   # False
print(a != b)   # True
print(a > b)    # True
```

---

## 3️⃣ Logical Operators

Logical operators multiple conditions ko combine karne ke liye use hote hain.

### `and` — Dono conditions True hon tabhi result True

```python
age = 25
has_ticket = True

if age >= 18 and has_ticket:
    print("You can enter the movie")
else:
    print("Entry denied")
```

### `or` — Koi bhi aik condition True ho to result True

```python
is_weekend = False
is_holiday = True

if is_weekend or is_holiday:
    print("No school today")
else:
    print("School as usual")
```

### `not` — Condition ko reverse (opposite) kar deta hai

```python
is_raining = False

if not is_raining:
    print("You can go outside")
else:
    print("Take an umbrella")
```

### Combining Multiple Logical Operators

```python
age = 20
has_license = True
has_car = False

if age >= 18 and has_license and not has_car:
    print("You can drive, but you need a car")
elif age >= 18 and has_license and has_car:
    print("You are ready to drive")
else:
    print("You cannot drive yet")
```

---

## 4️⃣ Truth Table (Quick Reference)

| A | B | A and B | A or B | not A |
|---|---|---------|--------|-------|
| True | True | True | True | False |
| True | False | False | True | False |
| False | True | False | True | True |
| False | False | False | False | True |

---

## ✅ Key Takeaways
- `if`, `elif`, `else` se program decisions leta hai
- Conditions banane ke liye comparison operators (`==`, `!=`, `>`, `<`, etc.) use hote hain
- `and` operator: dono conditions true honi chahiye
- `or` operator: sirf ek condition true honi chahiye
- `not` operator: condition ko reverse kar deta hai
- Nested `if` statements se complex decisions liye ja sakte hain

---

## 🔗 Practice Task
- User se uski age lo aur batao ke wo voter hai ya nahi (`age >= 18`)
- User se do numbers lo aur `and`/`or` use karke check karo ke dono positive hain ya nahi
- Ek simple login system banao jahan username aur password dono match hone chahiye (`and` operator use karke)
