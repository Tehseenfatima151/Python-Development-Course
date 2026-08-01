# Day 27 – GUI with Tkinter, Functions as Arguments & Miles-to-Km Converter

## 📌 Overview
Is session mein humne **Tkinter** seekha — Python ka built-in GUI (Graphical User Interface) library, jisse hum windows, buttons, labels, aur input fields wale desktop applications bana sakte hain. Sath hi humne dekha ke Python mein **functions khud bhi arguments ki tarah pass** ho sakte hain (jaise button ke `command` parameter mein) — ye concept GUI event-handling ka core hai. Iske baad humne ye sab use kar ke ek **Miles-to-Km Converter** app banayi.

---

## 1️⃣ What is Tkinter?

**Tkinter** Python ke sath **built-in** aata hai — koi extra install nahi karna parta. Isse hum desktop GUI apps bana sakte hain: windows, buttons, text fields, labels, waghera.

```python
import tkinter as tk

window = tk.Tk()
window.title("My App")
window.minsize(width=300, height=200)

window.mainloop()
```

**Explanation:**
- `tk.Tk()` — main application window banata hai
- `window.mainloop()` — **event loop** hai, jo window ko khula rakhta hai aur user actions (clicks, typing) ko sunta rehta hai

---

## 2️⃣ Widgets (Tkinter Ke Building Blocks)

### Label — Text Dikhane Ke Liye

```python
my_label = tk.Label(text="Hello, World!", font=("Arial", 24))
my_label.pack()
```

### Button — Click Karne Ke Liye

```python
my_button = tk.Button(text="Click Me")
my_button.pack()
```

### Entry — User Se Text Input Lene Ke Liye

```python
my_entry = tk.Entry(width=10)
my_entry.pack()

user_input = my_entry.get()
```

### Layout Managers — `pack()` vs `grid()`

```python
my_label.pack()
my_label.grid(column=0, row=0)
```

**Explanation:** `pack()` simple hai lekin control kam deta hai. `grid()` zyada precise row/column positioning deta hai — real apps mein zyada use hoti hai.

---

## 3️⃣ Functions as Arguments (Callbacks)

Python mein functions **khud bhi values hote hain** — is liye unhe kisi doosre function ko **argument ki tarah pass** kiya ja sakta hai, bina call kiye.

```python
def say_hello():
    print("Hello!")

my_button = tk.Button(text="Click Me", command=say_hello)
my_button.pack()
```

**Explanation:**
- `command=say_hello` — **function ka reference** diya hai, `say_hello()` nahi likha (bina brackets ke)
- Agar galti se `command=say_hello()` likh dete, to function **turant** call ho jata, na ke jab user click kare
- `command` parameter batata hai ke "jab click ho, tab ye function chalao" — ye ek **callback** hai

### Passing Arguments to Callbacks (Lambda)

```python
def greet(name):
    print(f"Hello, {name}!")

my_button = tk.Button(text="Greet", command=lambda: greet("Ali"))
my_button.pack()
```

**Explanation:** `lambda: greet("Ali")` ek chhota anonymous function banata hai jo click hone pe `greet("Ali")` call karta hai — is se arguments wale functions ko bhi safely `command` mein pass kar sakte hain.

---

## 4️⃣ Building the Miles-to-Km Converter

**Concept:** User Entry box mein miles enter karta hai, "Calculate" button dabata hai, aur uska equivalent kilometers ek Label mein show ho jata hai.

### Step 1: Window Setup

```python
import tkinter as tk

window = tk.Tk()
window.title("Mile to Km Converter")
window.config(padx=20, pady=20)
```

### Step 2: Miles Input (Entry) aur Label

```python
miles_input = tk.Entry(width=7)
miles_input.grid(column=1, row=0)

miles_label = tk.Label(text="Miles")
miles_label.grid(column=2, row=0)
```

### Step 3: Result Label (Jo Update Hoga)

```python
km_result_label = tk.Label(text="0")
km_result_label.grid(column=1, row=1)

is_equal_label = tk.Label(text="is equal to")
is_equal_label.grid(column=0, row=1)

km_label = tk.Label(text="Km")
km_label.grid(column=2, row=1)
```

### Step 4: Conversion Function

```python
def miles_to_km():
    miles = float(miles_input.get())
    km = round(miles * 1.609, 2)
    km_result_label.config(text=f"{km}")
```

**Explanation:**
- `miles_input.get()` — Entry box mein jo user ne likha hai, wo hamesha **string** ki soorat mein milta hai, is liye `float()` se convert kiya
- `1 mile = 1.609 km` — standard conversion formula
- `km_result_label.config(text=f"{km}")` — **existing** label ka text update kar deta hai, naya label banane ki zaroorat nahi

### Step 5: Calculate Button

```python
calculate_button = tk.Button(text="Calculate", command=miles_to_km)
calculate_button.grid(column=1, row=2)
```

### Step 6: Run the App

```python
window.mainloop()
```

---

## 5️⃣ Full Combined Program

```python
import tkinter as tk

window = tk.Tk()
window.title("Mile to Km Converter")
window.config(padx=20, pady=20)


def miles_to_km():
    miles = float(miles_input.get())
    km = round(miles * 1.609, 2)
    km_result_label.config(text=f"{km}")


miles_input = tk.Entry(width=7)
miles_input.grid(column=1, row=0)

miles_label = tk.Label(text="Miles")
miles_label.grid(column=2, row=0)

km_result_label = tk.Label(text="0")
km_result_label.grid(column=1, row=1)

is_equal_label = tk.Label(text="is equal to")
is_equal_label.grid(column=0, row=1)

km_label = tk.Label(text="Km")
km_label.grid(column=2, row=1)

calculate_button = tk.Button(text="Calculate", command=miles_to_km)
calculate_button.grid(column=1, row=2)

window.mainloop()
```

---

## 6️⃣ Bonus: Input Validation (Robust Version)

```python
def miles_to_km():
    try:
        miles = float(miles_input.get())
    except ValueError:
        km_result_label.config(text="Invalid input")
    else:
        km = round(miles * 1.609, 2)
        km_result_label.config(text=f"{km}")
```

**Explanation:** Agar user ne number ki jagah text likha, to `try-except` crash hone se bachata hai aur friendly error message dikhata hai.

---
## Screenshoot
<img width="964" height="705" alt="1" src="https://github.com/user-attachments/assets/1303114d-0706-4caa-bc60-bc26b8432e55" />

## ✅ Key Takeaways
- Tkinter Python ke sath built-in aata hai — window, labels, entries, buttons se GUI banane ke liye
- `window.mainloop()` GUI ko khula rakhta hai aur events sunta rehta hai
- `grid()` layout precise row/column positioning deta hai
- Functions **bina call kiye** kisi doosre function ko argument ki tarah pass kiye ja sakte hain — ye **callbacks** ka core concept hai
- Arguments wale functions ko callback banane ke liye `lambda` use karte hain
- `.config()` se kisi bhi widget ki property (text, color, etc.) baad mein update kar sakte hain
- `entry.get()` hamesha **string** deta hai, numeric operations ke liye convert karna zaroori hai

---

## 🔗 Practice Task
- Converter ko reverse bhi karo — Km input le kar Miles output de (dusra button add karo)
- Ek Temperature Converter banao (Celsius ↔ Fahrenheit) isi pattern se
- Input validation add karo taake negative numbers na accept hon
