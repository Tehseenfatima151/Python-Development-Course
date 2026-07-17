# Day 9 – Dictionaries, Nesting & Secret Auction Program

## 📌 Overview
Is session mein humne **dictionaries** ka detailed concept seekha — key-value pairs kya hote hain, unhe kaise create, access, aur modify karte hain, aur **nesting** (list ke andar dictionary, dictionary ke andar dictionary) kaise kaam karti hai. Iske baad humne ye concepts use kar ke ek practical **Secret Auction Program** banaya.

---

## 1️⃣ What is a Dictionary?

Dictionary Python ka data type hai jo data ko **key-value pairs** mein store karta hai — list ki tarah index (0,1,2...) ke bajaye hum apni khud ki **keys** define karte hain jo values se linked hoti hain.

```python
programming_dictionary = {
    "Bug": "An error in a program that prevents it from running as expected",
    "Function": "A piece of code that you can easily call over and over again",
}
```

**List vs Dictionary:**

| List | Dictionary |
|------|------------|
| `["apple", "banana"]` | `{"fruit1": "apple", "fruit2": "banana"}` |
| Index se access hoti hai (`list[0]`) | Key se access hoti hai (`dict["fruit1"]`) |
| Order matter karta hai | Key unique honi chahiye |

---

## 2️⃣ Creating & Accessing a Dictionary

```python
student = {
    "name": "Ali",
    "age": 22,
    "course": "Software Engineering"
}

print(student["name"])    # Output: Ali
print(student["age"])     # Output: 22
```

Agar key exist nahi karti to `KeyError` aayega:

```python
print(student["grade"])   # KeyError!
```

Is se bachne ke liye `.get()` method use karte hain:

```python
print(student.get("grade"))              # Output: None (error nahi aata)
print(student.get("grade", "Not Found")) # Output: Not Found (default value)
```

---

## 3️⃣ Adding, Updating & Removing Items

```python
student = {"name": "Ali", "age": 22}

# Naya key-value add karna
student["city"] = "Burewala"
print(student)   # {'name': 'Ali', 'age': 22, 'city': 'Burewala'}

# Existing value update karna
student["age"] = 23
print(student)   # {'name': 'Ali', 'age': 23, 'city': 'Burewala'}

# Item remove karna
del student["city"]
print(student)   # {'name': 'Ali', 'age': 23}
```

---

## 4️⃣ Looping through a Dictionary

```python
student = {"name": "Ali", "age": 22, "course": "Software Engineering"}

for key in student:
    print(key, ":", student[key])

# Output:
# name : Ali
# age : 22
# course : Software Engineering
```

Better tareeqa — `.items()` use kar ke:

```python
for key, value in student.items():
    print(f"{key} -> {value}")
```

---

## 5️⃣ Nesting (Dictionary ke andar Dictionary/List)

Nesting ka matlab hai ek data structure ke andar dusra data structure rakhna — jaise dictionary ke andar dictionary, ya list ke andar dictionary.

### Dictionary inside a Dictionary

```python
travel_log = {
    "France": {"visit_count": 12, "cities_visited": ["Paris", "Lille", "Dijon"]},
    "Germany": {"visit_count": 5, "cities_visited": ["Berlin", "Hamburg", "Stuttgart"]},
}

print(travel_log["France"]["cities_visited"])
# Output: ['Paris', 'Lille', 'Dijon']

print(travel_log["Germany"]["visit_count"])
# Output: 5
```

### List of Dictionaries

```python
students = [
    {"name": "Ali", "age": 22},
    {"name": "Sara", "age": 21},
    {"name": "Ahmed", "age": 23}
]

for student in students:
    print(f"{student['name']} is {student['age']} years old")

# Output:
# Ali is 22 years old
# Sara is 21 years old
# Ahmed is 23 years old
```

### Adding a New Nested Entry

```python
travel_log = {
    "France": {"visit_count": 12, "cities_visited": ["Paris", "Lille", "Dijon"]}
}

travel_log["Pakistan"] = {"visit_count": 1, "cities_visited": ["Lahore"]}
print(travel_log)
```

---

## 6️⃣ Secret Auction Program

**Concept:** Ye ek bidding program hai jahan multiple log apni secret bids dalte hain (dictionary mein name-bid store hota hai), aur akhir mein sirf **highest bidder** ka naam show hota hai — auction ka pura sach sirf tab pata chalta hai jab sab bid daal chuke hon.

### Step 1: Empty Dictionary Banana

```python
bids = {}
```

### Step 2: User se Name aur Bid Lena

```python
name = input("What is your name?: ")
price = int(input("What is your bid?: $"))

bids[name] = price
```

### Step 3: Multiple Bidders ke liye Loop + "Continue?" Logic

```python
bids = {}
bidding_finished = False

while not bidding_finished:
    name = input("What is your name?: ")
    price = int(input("What is your bid?: $"))

    bids[name] = price

    should_continue = input("Are there any other bidders? Type 'yes' or 'no': ").lower()
    if should_continue == "no":
        bidding_finished = True
```

### Step 4: Highest Bidder Nikalna (Function)

```python
def find_highest_bidder(bidding_record):
    highest_bid = 0
    winner = ""

    for bidder in bidding_record:
        bid_amount = bidding_record[bidder]
        if bid_amount > highest_bid:
            highest_bid = bid_amount
            winner = bidder

    print(f"The winner is {winner} with a bid of ${highest_bid}")
```

**Explanation:**
- `highest_bid` aur `winner` initially 0 aur empty rakhte hain
- Loop se har `bidder` (key) aur uska `bid_amount` (value) check hota hai
- Agar current bid pehle wali se zyada hai, to `highest_bid` aur `winner` update ho jate hain
- Loop khatam hone pe jo bhi sabse bara bid tha wo `winner` bacha hoga

### Step 5: Screen Clear Karna (Secret Rakhne ke liye)

Taake agla bidder pichli bids na dekh sake, screen clear karte hain:

```python
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
```

---

## 7️⃣ Full Combined Program

```python
def find_highest_bidder(bidding_record):
    highest_bid = 0
    winner = ""

    for bidder in bidding_record:
        bid_amount = bidding_record[bidder]
        if bid_amount > highest_bid:
            highest_bid = bid_amount
            winner = bidder

    print(f"The winner is {winner} with a bid of ${highest_bid}")


bids = {}
bidding_finished = False

print("Welcome to the Secret Auction Program")

while not bidding_finished:
    name = input("What is your name?: ")
    price = int(input("What is your bid?: $"))

    bids[name] = price

    should_continue = input("Are there any other bidders? Type 'yes' or 'no': ").lower()

    if should_continue == "no":
        bidding_finished = True
        find_highest_bidder(bids)
    elif should_continue == "yes":
        print("\n" * 20)   # Screen ko clear jaisa effect dene ke liye
```

---

## 8️⃣ Example Run

```
Welcome to the Secret Auction Program
What is your name?: Ali
What is your bid?: $500
Are there any other bidders? Type 'yes' or 'no': yes

What is your name?: Sara
What is your bid?: $750
Are there any other bidders? Type 'yes' or 'no': yes

What is your name?: Ahmed
What is your bid?: $300
Are there any other bidders? Type 'yes' or 'no': no

The winner is Sara with a bid of $750
```

---

## ✅ Key Takeaways
- Dictionary key-value pairs mein data store karti hai; keys unique honi chahiye
- `.get()` method safe access deta hai bina `KeyError` ke
- `.items()` se dictionary ke keys aur values dono ek sath loop mein milte hain
- Nesting se hum dictionary ke andar dictionary/list, ya list ke andar dictionary rakh sakte hain (real-world data jaisa structure)
- Secret Auction program dictionaries + loops + functions + conditionals ka real combination hai
- Highest value nikalne ka pattern: aik variable ko 0/empty se start karo, loop mein compare karte jao, jo bara mile usse update kar do

---

## 🔗 Practice Task
- Auction program mein validation add karo taake bid negative na ho sake
- Ek nested dictionary banao jo class ke students aur unke marks store kare, phir highest scorer nikalo
- Auction program ko modify karo taake top 3 bidders show ho (sirf ek winner ki bajaye)
