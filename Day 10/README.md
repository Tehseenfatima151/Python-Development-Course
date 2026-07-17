# Day 10 – Functions with Outputs, Docstrings & Calculator Program

## 📌 Overview
Is session mein humne **functions with outputs (return values)** ka detailed concept seekha — function se value kaise return hoti hai, multiple return statements kaise kaam karte hain, aur **docstrings** kya hote hain jo function ko document karne ke liye use hote hain. Iske baad humne ye sab concepts combine kar ke ek working **Calculator Program** banaya.

---

## 1️⃣ Functions with Outputs (Return Values)

Pichle sessions mein humne functions dekhe jo sirf `print()` karte thay. Lekin agar hum chahte hain ke function ka result **aage kisi variable mein store ho ya kisi aur calculation mein use ho**, to hume `return` statement use karna parta hai.

```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)   # Output: 8
```

`print()` sirf screen pe dikhata hai — usse function se bahar use nahi kiya ja sakta. `return` value ko actually function se bahar bhej deta hai.

```python
def multiply(a, b):
    print(a * b)      # sirf print karta hai, value return nahi hoti

x = multiply(4, 5)    # Output: 20 (print ho jata hai)
print(x)               # Output: None (kyunke return nahi kiya)
```

---

## 2️⃣ Multiple Return Values

Python mein function ek sath **multiple values** bhi return kar sakta hai (comma se separate kar ke) — ye tuple ki tarah return hoti hain.

```python
def calculate(a, b):
    total = a + b
    difference = a - b
    return total, difference

sum_result, diff_result = calculate(10, 4)
print(sum_result)    # Output: 14
print(diff_result)   # Output: 6
```

---

## 3️⃣ Conditional Return (if-else ke sath)

Function ke andar condition ke hisaab se different values return ki ja sakti hain.

```python
def check_even_odd(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

print(check_even_odd(7))    # Output: Odd
print(check_even_odd(10))   # Output: Even
```

⚠️ Jaise hi `return` statement execute hota hai, function turant **exit** ho jata hai — uske baad ka code us call ke liye run nahi hota.

```python
def test(number):
    if number > 0:
        return "Positive"
    return "Not Positive"   # sirf tab chalega jab upar wala return na chala ho
```

---

## 4️⃣ Docstrings

**Docstring** ek documentation string hoti hai jo function ke bilkul shuru mein triple quotes (`"""..."""`) mein likhi jati hai. Ye batati hai ke function kya karta hai, kya parameters leta hai, aur kya return karta hai.

```python
def calculate_bmi(weight, height):
    """
    Calculates the Body Mass Index (BMI).

    Parameters:
    weight (float): Weight in kilograms
    height (float): Height in meters

    Returns:
    float: The calculated BMI rounded to 2 decimal places
    """
    bmi = weight / (height ** 2)
    return round(bmi, 2)
```

**Docstring ke fayde:**
- Function ka purpose turant samajh aata hai bina code parhe
- `help()` function se docstring dekhi ja sakti hai
- Bare projects aur teams mein code samajhna asaan ho jata hai
- Professional aur readable code likhne ki adat banti hai

```python
help(calculate_bmi)
# Output: Docstring ka pura content show ho jayega
```

**Simple one-line docstring bhi ho sakti hai:**

```python
def greet(name):
    """Prints a greeting message with the given name."""
    print(f"Hello, {name}!")
```

---

## 5️⃣ Building the Calculator Program

### Step 1: Basic Operation Functions (with return)

```python
def add(n1, n2):
    """Returns the sum of two numbers."""
    return n1 + n2

def subtract(n1, n2):
    """Returns the result of subtracting n2 from n1."""
    return n1 - n2

def multiply(n1, n2):
    """Returns the product of two numbers."""
    return n1 * n2

def divide(n1, n2):
    """Returns the result of dividing n1 by n2."""
    return n1 / n2
```

### Step 2: Dictionary to Map Symbols to Functions

Ye ek useful trick hai — operators (`"+"`, `"-"`, etc.) ko directly functions se link kar dete hain dictionary ke through:

```python
operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide
}
```

### Step 3: Calculator Logic

```python
def calculator():
    print("Welcome to the Python Calculator!")

    num1 = float(input("Enter the first number: "))

    for symbol in operations:
        print(symbol)

    should_continue = True

    while should_continue:
        operation_symbol = input("Pick an operation: ")
        num2 = float(input("Enter the next number: "))

        calculation_function = operations[operation_symbol]
        answer = calculation_function(num1, num2)

        print(f"{num1} {operation_symbol} {num2} = {answer}")

        choice = input(f"Type 'y' to continue calculating with {answer}, or 'n' to start new calculation: ").lower()

        if choice == "y":
            num1 = answer
        else:
            should_continue = False
            print("\n" * 2)
            calculator()   # Naya calculator session shuru karna
```

**Explanation:**
- `operations` dictionary se symbol ke through seedha uska function nikal lete hain (`operations["+"]` → `add` function)
- `calculation_function(num1, num2)` — ye function ko dynamically call karta hai, jo bhi symbol choose hua ho
- Agar user 'y' bole to current answer ko `num1` bana kar loop chalta rehta hai (chaining calculations)
- 'n' bolne pe naya session shuru ho jata hai (`calculator()` khud ko dobara call karta hai — isse **recursion** kehte hain)

### Step 4: Full Combined Program

```python
def add(n1, n2):
    """Returns the sum of two numbers."""
    return n1 + n2

def subtract(n1, n2):
    """Returns the result of subtracting n2 from n1."""
    return n1 - n2

def multiply(n1, n2):
    """Returns the product of two numbers."""
    return n1 * n2

def divide(n1, n2):
    """Returns the result of dividing n1 by n2."""
    return n1 / n2

operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide
}

def calculator():
    print("Welcome to the Python Calculator!")
    num1 = float(input("Enter the first number: "))

    for symbol in operations:
        print(symbol)

    should_continue = True

    while should_continue:
        operation_symbol = input("Pick an operation: ")
        num2 = float(input("Enter the next number: "))
        calculation_function = operations[operation_symbol]
        answer = calculation_function(num1, num2)

        print(f"{num1} {operation_symbol} {num2} = {answer}")

        choice = input(f"Type 'y' to continue with {answer}, or 'n' to start new calculation: ").lower()

        if choice == "y":
            num1 = answer
        else:
            should_continue = False
            print("\n" * 2)
            calculator()

calculator()
```

---

## 6️⃣ Example Run

```
Welcome to the Python Calculator!
Enter the first number: 10
+
-
*
/
Pick an operation: +
Enter the next number: 5
10.0 + 5.0 = 15.0
Type 'y' to continue with 15.0, or 'n' to start new calculation: y
Pick an operation: *
Enter the next number: 2
15.0 * 2.0 = 30.0
```

---

## ✅ Key Takeaways
- `return` function se value bahar bhejta hai jo aage store/use ho sakti hai; `print()` sirf dikhata hai
- Ek function multiple values bhi comma se separate kar ke return kar sakta hai
- `return` execute hote hi function turant exit ho jata hai
- Docstrings (`"""..."""`) function ke shuru mein likhi jati hain aur `help()` se dekhi ja sakti hain — code ko professional aur readable banati hain
- Dictionary mein functions ko values ki tarah store karna aik powerful pattern hai (symbol → function mapping)
- Function ka khud ko call karna **recursion** kehlata hai — calculator program mein naya session start karne ke liye use hua

---

## 🔗 Practice Task
- Calculator mein power (`**`) aur modulus (`%`) operations bhi add karo
- Divide function mein zero division error handle karo (agar `n2 == 0` ho to error message do)
- Har function mein proper docstring likho jisme parameters aur return type dono mention hon
