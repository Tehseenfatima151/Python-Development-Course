# Day 6 – Functions, Code Blocks & Reeborg's World (Hurdles + Maze)

## 📌 Overview
Is session mein humne **functions** ka concept detail mein seekha — function kya hota hai, kaise banate hain, parameters aur return values kaise kaam karte hain, aur **code blocks/indentation** ki importance samjhi. Iske baad humne ye concepts practically **Reeborg's World** mein apply kiye — jahan robot ko hurdles cross karwane aur maze solve karwane ke liye functions aur loops ka logic banaya.

---

## 1️⃣ What is a Function?

Function ek reusable block of code hota hai jo ek specific task perform karta hai. Isse hum code ko baar baar likhne ke bajaye ek jagah define kar ke jitni baar chahen call kar sakte hain.

**Function use karne ke fayde:**
- Code repeat nahi karna parta (DRY principle – Don't Repeat Yourself)
- Code organized aur readable hota hai
- Bugs fix karna asaan ho jata hai (sirf ek jagah change karo)
- Large programs ko chote manageable pieces mein tor sakte hain

---

## 2️⃣ Defining a Function

Function `def` keyword se define hota hai.

```python
def greet():
    print("Hello, welcome to Python!")

greet()   # Function ko call karna
# Output: Hello, welcome to Python!
```

Function tab tak run nahi hota jab tak usse **call** na kiya jaye.

---

## 3️⃣ Code Blocks & Indentation

Python mein code block (function, if, loop, etc. ke andar wala code) **indentation** (spaces) se define hota hai — curly braces `{}` nahi hote jaisa dusri languages mein hota hai.

```python
def check_age(age):
    if age >= 18:
        print("You are an adult")   # yeh if block ke andar hai
    else:
        print("You are a minor")    # yeh else block ke andar hai
    print("Age check complete")      # yeh function block ke andar hai, if-else se bahar
```

⚠️ **Indentation galat hone se `IndentationError` aata hai** — is liye Python mein spacing bohot important hoti hai.

---

## 4️⃣ Parameters & Arguments

Function ko dynamic banane ke liye hum usme **parameters** de sakte hain — ye function ke andar use hone wale placeholder variables hote hain.

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Ali")     # Output: Hello, Ali!
greet("Sara")    # Output: Hello, Sara!
```

**Multiple parameters:**

```python
def add_numbers(a, b):
    print(f"Sum is: {a + b}")

add_numbers(5, 3)   # Output: Sum is: 8
```

**Default parameters** (agar value na di jaye to default use hoti hai):

```python
def greet(name="Guest"):
    print(f"Hello, {name}!")

greet()          # Output: Hello, Guest!
greet("Ahmed")   # Output: Hello, Ahmed!
```

---

## 5️⃣ Return Values

`return` statement function se value **wapis bhejta** hai taake usse aage use kiya ja sake. `print()` sirf screen pe dikhata hai, jabke `return` value ko actually deta hai.

```python
def add_numbers(a, b):
    return a + b

result = add_numbers(4, 6)
print(result)    # Output: 10
print(result * 2)  # Output: 20  (return ki hui value use ho sakti hai)
```

**Function bina return ke `None` deta hai:**

```python
def say_hi():
    print("Hi!")

output = say_hi()
print(output)   # Output: Hi!  followed by  None
```

---

## 6️⃣ Why Functions Matter (Real Example)

```python
# Bina function ke - code repeat ho raha hai
print("Area of rectangle 1:", 5 * 3)
print("Area of rectangle 2:", 8 * 2)
print("Area of rectangle 3:", 10 * 4)

# Function ke sath - clean aur reusable
def rectangle_area(length, width):
    return length * width

print("Area of rectangle 1:", rectangle_area(5, 3))
print("Area of rectangle 2:", rectangle_area(8, 2))
print("Area of rectangle 3:", rectangle_area(10, 4))
```

---

## 7️⃣ Reeborg's World — Hurdle Game

**Reeborg's World** ek visual programming environment hai jahan hum ek robot ko commands de kar move karwate hain — `move()`, `turn_left()`, `front_is_clear()` jaisi built-in functions use hoti hain. Hurdle challenges mein robot ko raste mein aane wale obstacles (hurdles) cross karne hote hain.

### Basic Movement Commands

```python
move()          # Robot ko ek step aage move karta hai
turn_left()      # Robot ko left taraf ghumata hai
```

### Jump Over One Hurdle (custom function bana kar)

Reeborg mein sidha "jump" command nahi hoti, is liye hum apni khud ki function banate hain jo turn_left ko 3 baar call kar ke right turn create karti hai, aur hurdle cross karti hai:

```python
def turn_right():
    turn_left()
    turn_left()
    turn_left()

def jump():
    turn_left()
    move()
    turn_right()
    move()
    turn_right()
    move()
    turn_left()

jump()   # Ek hurdle cross ho jayega
```

### Multiple Hurdles — Loop ke sath

Agar raste mein bohot saare hurdles hain aur pata nahi kitne hain, to `front_is_clear()` condition check karte hain:

```python
def turn_right():
    turn_left()
    turn_left()
    turn_left()

def jump():
    turn_left()
    move()
    turn_right()
    move()
    turn_right()
    move()
    turn_left()

while not at_goal():
    if front_is_clear():
        move()
    else:
        jump()
```

**Explanation:**
- `while not at_goal()` — jab tak robot goal (finish point) tak nahi pohanchta, loop chalta rahega
- `front_is_clear()` — agar aage rasta clear hai to seedha `move()`
- Agar clear nahi hai (matlab hurdle hai) to `jump()` function call ho ga

---

## 8️⃣ Reeborg's World — Maze Solving

Maze solve karne ke liye robot ko diwaron (walls) ke sath chalna hota hai jab tak goal na mil jaye. Ye "wall follower" algorithm kehlata hai.

```python
def turn_right():
    turn_left()
    turn_left()
    turn_left()

def right_is_clear():
    turn_right()
    clear = front_is_clear()
    turn_left()
    return clear

while not at_goal():
    if right_is_clear():
        turn_right()
        move()
    elif front_is_clear():
        move()
    else:
        turn_left()
```

**Explanation (Right-Hand Rule / Wall Follower Logic):**
1. Sabse pehle check karo ke **right** side clear hai ya nahi (custom `right_is_clear()` function se)
2. Agar right clear hai → right turn kar ke move karo (hamesha right wall follow karna)
3. Agar right clear nahi lekin **front** clear hai → seedha move karo
4. Agar dono blocked hain → left turn karo (naya rasta dhoondo)
5. Ye loop tab tak chalta hai jab tak `at_goal()` True na ho jaye

Is technique se robot khud ba khud diwaron ko follow karte hue maze ke andar se rasta dhoond kar goal tak pohanch jata hai — chahe maze kitna bhi complex ho.

---

## ✅ Key Takeaways
- Functions code ko reusable, organized aur readable banate hain
- `def` keyword se function define hota hai, call kiye bina wo run nahi hota
- Parameters function ko dynamic banate hain, `return` value wapis bhejta hai
- Python mein code blocks indentation se define hote hain — spacing ka strict rehna zaroori hai
- Reeborg's World mein custom functions (jaise `turn_right()`, `jump()`) bana kar complex robot movements simplify kiye ja sakte hain
- Hurdle games mein `front_is_clear()` check karke conditional jump logic banaya
- Maze solving mein "wall follower" algorithm use hota hai jisme robot hamesha ek taraf (right) ki wall follow karta hai jab tak goal na mil jaye

---

## 🔗 Practice Task
- Apna khud ka `turn_around()` function banao jo robot ko 180 degree ghuma de
- Hurdle game ko modify karo taake robot hurdles ke darmiyan coins bhi collect kare
- Maze solving logic ko left-hand wall follower mein convert karo (right ki bajaye left wall follow kare)
