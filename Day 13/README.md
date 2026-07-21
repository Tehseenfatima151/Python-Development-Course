# Day 13 – Debugging in Python (Finding & Fixing Bugs)

## 📌 Overview
Is session mein humne **debugging** ka detailed concept seekha — bug kya hota hai, errors ko kaise identify karte hain, aur unhe systematically kaise fix karte hain. Debugging aik programmer ki sabse important skill hai — chahe kitna bhi acha code likho, bugs zaroor aate hain, asal maharat unhe dhoondne aur theek karne mein hai.

---

## 1️⃣ What is a Bug?

**Bug** kisi program mein woh error ya mistake hota hai jiski wajah se program ya to crash ho jata hai, ya expected output nahi deta. Naam ka origin dilchasp hai — purane computers mein literally aik keere (moth) ne machine mein malfunction create kiya tha, is liye "bug" naam mash-hoor ho gaya.

**Bugs 3 tarah ke hote hain:**

| Type | Description | Example |
|------|-------------|---------|
| **Syntax Error** | Code Python ke rules follow nahi karta | Missing colon, galat indentation |
| **Runtime Error** | Program chalte waqt crash ho jata hai | Divide by zero, wrong data type |
| **Logical Error** | Program chalta hai lekin galat result deta hai | Galat formula, galat condition |

---

## 2️⃣ Syntax Errors

Ye sabse asaan errors hote hain pakadna, kyunke Python khud batata hai kahan galti hai — program run hi nahi hota jab tak fix na ho.

```python
def greet()
    print("Hello")
```

```
SyntaxError: expected ':'
```

**Fix:** Function definition ke baad colon zaroori hai:

```python
def greet():
    print("Hello")
```

**Common Syntax Errors:**
- Colon (`:`) missing hona if/for/while/def ke baad
- Indentation galat hona
- Brackets/quotes match na hona
- `=` aur `==` mein confusion (assignment vs comparison)

---

## 3️⃣ Runtime Errors (Exceptions)

Ye errors program chalte waqt aate hain — syntax sahi hoti hai lekin execution ke dauran kuch galat ho jata hai.

```python
number = int(input("Enter a number: "))
result = 10 / number
print(result)
```

Agar user `0` enter kare:
```
ZeroDivisionError: division by zero
```

**Common Runtime Errors:**

| Error | Kab Aata Hai |
|-------|--------------|
| `NameError` | Undefined variable use karna |
| `TypeError` | Galat data type pe operation (e.g. string + int) |
| `IndexError` | List ka aisa index access karna jo exist nahi karta |
| `KeyError` | Dictionary mein aisi key dhoondna jo exist nahi karti |
| `ValueError` | Function ko galat type ki value milna (e.g. `int("abc")`) |
| `ZeroDivisionError` | Kisi number ko 0 se divide karna |

```python
fruits = ["apple", "banana"]
print(fruits[5])
# IndexError: list index out of range
```

---

## 4️⃣ Logical Errors (Sabse Mushkil)

Ye sabse tricky bugs hote hain kyunke Python koi error message nahi deta — program chalta hai, lekin result galat hota hai.

```python
def calculate_average(numbers):
    total = sum(numbers)
    average = total / len(numbers) - 1   # Bug: galat formula (-1 extra hai)
    return average

print(calculate_average([10, 20, 30]))
# Output: 19.0  (galat! sahi average 20.0 hona chahiye)
```

Aise bugs sirf **testing aur careful checking** se pakde jate hain — Python khud nahi bata sakta ke formula logically galat hai.

---

## 5️⃣ How to Debug: Step-by-Step Methods

### Method 1: Read the Error Message Carefully

Python ka error message (Traceback) bohot kuch batata hai:
- Kaunsi file aur **line number** pe error hai
- Kaunsa **error type** hai
- Ek **description** ke sath ke asal masla kya hai

```
Traceback (most recent call last):
  File "main.py", line 5, in <module>
    print(fruits[5])
IndexError: list index out of range
```

Yahan hume seedha line 5 pe dekhne ki zaroorat hai — error message ko ignore mat karo, ye 90% waqt exact masla bata deta hai.

---

### Method 2: Print Statement Debugging

Sabse basic aur useful technique — code ke beech beech mein `print()` laga kar dekho ke variables ki value kya hai.

```python
def calculate_total(price, quantity):
    print(f"DEBUG: price = {price}, quantity = {quantity}")
    total = price * quantity
    print(f"DEBUG: total = {total}")
    return total

calculate_total(50, "3")
```

Is se pata chal jayega ke `quantity` string hai instead of number — jo bug ki wajah ban sakta hai.

---

### Method 3: Using a Debugger (Breakpoints)

Modern code editors (VS Code, PyCharm) mein **debugger** hota hai jisse hum:
- Code mein **breakpoint** laga sakte hain (ek line jahan program pause ho jaye)
- Har variable ki current value dekh sakte hain
- Code ko **line by line (step through)** chala kar dekh sakte hain ke exact kahan cheez galat ho rahi hai

```python
def add_numbers(a, b):
    result = a + b   # <- yahan breakpoint laga do
    return result

add_numbers(5, "3")
```

Breakpoint pe program ruk jayega aur hum dekh sakenge ke `b` string hai, int nahi — is se bug turant clear ho jata hai bina bohot saare print statements likhe.

---

### Method 4: Divide and Conquer (Isolate the Problem)

Agar program bara hai aur pata nahi kahan bug hai, to code ko chote hisso mein tor kar test karo:

```python
# Puri chain ki bajaye har step alag se check karo
data = fetch_data()
print(data)          # Step 1 check

processed = process_data(data)
print(processed)     # Step 2 check

result = analyze(processed)
print(result)        # Step 3 check
```

Jahan output ghalat aana shuru ho, wahi function culprit hai.

---

### Method 5: Rubber Duck Debugging

Ye ek famous technique hai jisme hum apna code line-by-line **kisi ko (ya khud ko, ya literally aik rubber duck ko!) zabani explain** karte hain. Explain karte waqt aksar khud hi pata chal jata hai ke logic mein kya masla hai — kyunke jab hum khud ko samjhate hain to dimagh detail mein sochta hai.

---

### Method 6: Testing with Known Inputs

Function ko aise input do jiska answer tumhe pehle se pata ho, taake verify kar sako ke function sahi kaam kar raha hai ya nahi.

```python
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

# Known test case: average of [10, 20, 30] should be 20
print(calculate_average([10, 20, 30]))   # Expected: 20.0
```

Agar output expected se match na kare, to bug confirm ho jata hai.

---

### Method 7: Check Data Types

Bohot saare bugs galat data type ki wajah se hote hain — `type()` function se check karna helpful hota hai.

```python
age = input("Enter your age: ")
print(type(age))   # <class 'str'> - yaad rahe input() hamesha string deta hai!

age = int(age)
print(type(age))   # <class 'int'>
```

---

## 6️⃣ Common Beginner Mistakes (Checklist)

Jab bug na mile, ye cheezein check karo:

- ✅ Indentation sahi hai? (spaces consistent hain)
- ✅ `=` (assignment) aur `==` (comparison) mix to nahi ho gaye?
- ✅ List/string index range ke andar hai?
- ✅ Variable ka naam sahi spell hua hai? (typos)
- ✅ Function `return` kar raha hai ya sirf `print` kar raha hai?
- ✅ Loop ka condition kabhi `False` bhi hota hai ya infinite loop ban gaya?
- ✅ Data type expected type ke hi hai? (string vs int confusion)
- ✅ Dictionary/list ki key ya index waqai exist karti hai?

---

## 7️⃣ Example: Full Debugging Process

**Buggy Code:**

```python
def calculate_discount(price, discount_percent):
    discount = price * discount_percent / 100
    final_price = price - discount
    return final_price

items = [{"name": "Shirt", "price": 1000}, {"name": "Shoes", "price": 3000}]

for item in items:
    discounted = calculate_discount(item["price"], "10")
    print(f"{item['name']}: {discounted}")
```

**Error:**
```
TypeError: unsupported operand type(s) for /: 'int' and 'str'
```

**Debugging Steps:**
1. **Error message parho** — batata hai ke divide operation mein int aur str ka mismatch hai
2. **Line number check karo** — `discount = price * discount_percent / 100` pe issue hai
3. **Print statement lagao** — `print(type(discount_percent))` daal ke dekho, pata chalega ye `str` hai
4. **Root cause dhoondo** — function call mein `"10"` string ke roop mein pass kiya gaya tha, number ki bajaye
5. **Fix karo:**

```python
discounted = calculate_discount(item["price"], 10)   # Ab int hai, string nahi
```

---

## ✅ Key Takeaways
- Bugs 3 types ke hote hain: Syntax (Python khud pakarta hai), Runtime (execution ke dauran crash), aur Logical (chalta hai lekin galat result deta hai)
- Error message hamesha carefully parhna chahiye — line number aur error type dono useful clues dete hain
- `print()` statements sabse simple aur effective debugging tool hain
- Debugger tools (breakpoints) se code line-by-line trace kar ke exact problem dhoondi ja sakti hai
- Bara code hamesha chote hisso mein tor kar test karo (divide and conquer)
- Rubber duck debugging — apna code zabani explain karna khud hi bug samajhne mein madad karta hai
- Known test cases se function ki correctness verify karo
- `type()` se data type mismatches jaldi pakde ja sakte hain

---

## 🔗 Practice Task
- Ek purana program (jaise Hangman ya Calculator) uthao aur usme jaan bujh kar 3 different bugs (syntax, runtime, logical) daalo, phir unhe fix karo
- Kisi function mein print-statement debugging use kar ke pata lagao ke variable kis point pe galat value le raha hai
- Apne code editor mein breakpoint laga kar dekho ke debugger kaise step-by-step execution dikhata hai
