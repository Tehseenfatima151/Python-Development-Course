# Day 26 – List & Dict Comprehension + NATO Alphabet Project

## 📌 Overview
Is session mein humne **List Comprehension** aur **Dict Comprehension** seekha — Python ka ek concise, elegant tareeqa jisse loops se lists/dictionaries banane ka code **ek hi line** mein likha ja sakta hai. Iske baad humne ye concept use kar ke **NATO Phonetic Alphabet** program banaya — jo kisi bhi word ka har letter uske corresponding NATO code (jaise A → Alpha, B → Bravo) mein convert karta hai.

---

## 1️⃣ What is List Comprehension?

**List Comprehension** ek **compact tareeqa** hai list banane ka — traditional `for` loop ke bajaye **ek line** mein.

### Traditional Way (For Loop)

```python
numbers = [1, 2, 3, 4, 5]
squared = []

for num in numbers:
    squared.append(num ** 2)

print(squared)   # [1, 4, 9, 16, 25]
```

### List Comprehension Way

```python
numbers = [1, 2, 3, 4, 5]
squared = [num ** 2 for num in numbers]
print(squared)   # [1, 4, 9, 16, 25]
```

**Syntax:** `[expression for item in iterable]`

---

## 2️⃣ List Comprehension with Condition (Filtering)

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

even_numbers = [num for num in numbers if num % 2 == 0]
print(even_numbers)   # [2, 4, 6, 8, 10]
```

**Syntax:** `[expression for item in iterable if condition]`

### With Condition + Else (Ternary Style)

```python
numbers = [1, 2, 3, 4, 5]

labels = ["even" if num % 2 == 0 else "odd" for num in numbers]
print(labels)   # ['odd', 'even', 'odd', 'even', 'odd']
```

**Explanation:** Jab `if-else` dono hon, to unhe **expression se pehle** likhte hain (filter wale `if` se position alag hoti hai).

---

## 3️⃣ List Comprehension on Strings

```python
word = "hello"
letters = [letter for letter in word]
print(letters)   # ['h', 'e', 'l', 'l', 'o']
```

**Explanation:** String bhi ek iterable hai, is liye list comprehension usse bhi loop kar sakti hai — har character ek list item ban jata hai.

---

## 4️⃣ List Comprehension over a Dictionary

```python
student_scores = {"Ali": 85, "Sara": 92, "Ahmed": 78}

names = [key for (key, value) in student_scores.items()]
print(names)   # ['Ali', 'Sara', 'Ahmed']

passed = [name for (name, score) in student_scores.items() if score >= 80]
print(passed)   # ['Ali', 'Sara']
```

**Explanation:** `.items()` se dictionary ke key-value pairs milte hain — list comprehension unhe unpack kar ke filter/transform kar sakti hai.

---

## 5️⃣ What is Dict Comprehension?

**Dict Comprehension** bilkul list comprehension jaisi hi hai, bas iska output ek **dictionary** hota hai, list nahi.

```python
numbers = [1, 2, 3, 4, 5]

squared_dict = {num: num ** 2 for num in numbers}
print(squared_dict)   # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

**Syntax:** `{key_expression: value_expression for item in iterable}`

### Dict Comprehension from an Existing Dictionary

```python
student_scores = {"Ali": 85, "Sara": 92, "Ahmed": 78}

bonus_scores = {name: score + 5 for (name, score) in student_scores.items()}
print(bonus_scores)   # {'Ali': 90, 'Sara': 97, 'Ahmed': 83}
```

### Dict Comprehension with Condition

```python
weather_data = {"Monday": 68, "Tuesday": 65, "Wednesday": 70, "Thursday": 62}

hot_days = {day: temp for (day, temp) in weather_data.items() if temp > 65}
print(hot_days)   # {'Wednesday': 70, 'Monday': 68}
```

---

## 6️⃣ Building the NATO Alphabet Project

**Concept:** NATO Phonetic Alphabet mein har letter ka ek unique word hota hai (taake radio/phone pe confusion na ho) — jaise "A" ke liye "Alpha", "B" ke liye "Bravo". Humne is project mein CSV se ye data load kiya aur **dict comprehension** use kar ke ek lookup dictionary banai, phir user ke diye gaye word ko NATO codes mein convert kiya.

### Step 1: NATO Data (CSV se — `nato_phonetic_alphabet.csv`)

```
letter,code
A,Alpha
B,Bravo
C,Charlie
D,Delta
...
Z,Zulu
```

### Step 2: CSV ko Dictionary Mein Convert Karna (Dict Comprehension)

```python
import pandas as pd

data = pd.read_csv("nato_phonetic_alphabet.csv")

nato_dict = {row.letter: row.code for (index, row) in data.iterrows()}
print(nato_dict)
# {'A': 'Alpha', 'B': 'Bravo', 'C': 'Charlie', ...}
```

**Explanation:**
- `data.iterrows()` — pandas DataFrame ki har row pe loop chalata hai, `index` aur `row` dono deta hai
- Dict comprehension se hum seedha ek `letter → code` **lookup dictionary** bana lete hain — bina manual `for` loop aur `dict[key] = value` likhe

### Step 3: User Input Ko NATO Codes Mein Convert Karna (List Comprehension)

```python
word = input("Enter a word: ").upper()

output_list = [nato_dict[letter] for letter in word]
print(output_list)
```

**Explanation:**
- `.upper()` — user ka input uppercase mein convert karte hain, kyunke dictionary ki keys bhi uppercase hain
- List comprehension **har letter** ko `word` se le kar `nato_dict` mein dhoondti hai aur uska corresponding code list mein daal deti hai

```python
# Traditional equivalent (bina comprehension ke)
output_list = []
for letter in word:
    output_list.append(nato_dict[letter])
```

---

## 7️⃣ Full Combined Program

```python
import pandas as pd

data = pd.read_csv("nato_phonetic_alphabet.csv")

nato_dict = {row.letter: row.code for (index, row) in data.iterrows()}

word = input("Enter a word: ").upper()

output_list = [nato_dict[letter] for letter in word]
print(output_list)
```

---

## 8️⃣ Handling Invalid Characters (Robust Version)

Agar user koi number ya symbol type kare, to `nato_dict[letter]` **KeyError** dega. Isse handle karne ke liye:

```python
def generate_nato():
    word = input("Enter a word: ").upper()
    try:
        output_list = [nato_dict[letter] for letter in word if letter.isalpha()]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        generate_nato()
    else:
        print(output_list)

generate_nato()
```

**Explanation:** `if letter.isalpha()` list comprehension ke andar hi ek extra filter add kar deta hai — sirf **letters** hi consider hote hain, numbers/symbols automatically skip ho jate hain.

---

## 9️⃣ Example Run

```
Enter a word: PYTHON
['Papa', 'Yankee', 'Tango', 'Hotel', 'Oscar', 'November']
```
## Screenshoot
<img width="810" height="708" alt="1" src="https://github.com/user-attachments/assets/2ece80a4-094c-470c-9a12-f299f964366a" />

---

## ✅ Key Takeaways
- List comprehension `[expression for item in iterable if condition]` — loops ko concise, readable ek-line code mein badalti hai
- Dict comprehension isi tarah kaam karti hai, bas `{key: value for ...}` format mein — dictionary output deti hai
- Comprehensions **filtering** (`if`) aur **transformation** (expression) dono ek sath kar sakti hain
- `data.iterrows()` se pandas DataFrame ki rows pe loop chala kar dict comprehension se lookup dictionary banana ek common, powerful pattern hai
- Comprehensions code ko chota to karti hain, lekin agar logic complex ho jaye to readability ke liye traditional loop better ho sakta hai — balance zaroori hai

---

## 🔗 Practice Task
- Ek dict comprehension banao jo `student_scores` dictionary ko grades (A/B/C/F) mein convert kare, based on score ranges
- NATO program mein spaces bhi handle karo (multi-word input ke liye)
- List comprehension se ek list banao jo 1-100 tak sirf un numbers ki ho jo 3 aur 5 dono se divisible hon
