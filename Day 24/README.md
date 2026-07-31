# Day 24 – Working with Local Files, Directories & Mail Merge Project

## 📌 Overview

Day 24 mein Python ke **local files aur directories ke sath kaam karna** seekha. Is din ka main focus tha ke Python ke through files ko read karna, write karna, paths ko handle karna aur directories ke andar files ko access karna.

Iske sath ek practical **Mail Merge Project** banaya jisme ek template letter ko multiple people ke names ke sath automatically generate kiya gaya.

Ye project especially **file handling, string manipulation, loops aur automation** ko practically samajhne ke liye useful tha.

---

## 1️⃣ Topics Covered

Day 24 mein ye important concepts seekhe:

* 📁 Working with directories
* 📄 Reading files
* ✍️ Writing files
* 🔄 Reading and processing multiple lines
* 📍 File paths
* 🗂️ Relative paths
* 📝 String replacement
* 🔁 Loops ke through multiple files generate karna
* 🤖 Basic automation using Python
* 📬 Mail Merge Project

---

## 2️⃣ Project Structure

```text
day24/
├── main.py
├── Input/
│   ├── Letters/
│   │   └── starting_letter.txt
│   └── Names/
│       └── invited_names.txt
│
└── Output/
    └── ReadyToSend/
        ├── letter_for_Alex.txt
        ├── letter_for_Ben.txt
        └── letter_for_Charlie.txt
```

| File / Folder         | Responsibility                             |
| --------------------- | ------------------------------------------ |
| `main.py`             | Main Python program                        |
| `Input/Names/`        | Names ki list contain karta hai            |
| `Input/Letters/`      | Letter ka template contain karta hai       |
| `Output/ReadyToSend/` | Final personalized letters store karta hai |

---

## 3️⃣ Reading a File

Python mein kisi file ko read karne ke liye `open()` function use kar sakte hain.

```python
with open("my_file.txt") as file:
    contents = file.read()

print(contents)
```

### Explanation:

```python
open("my_file.txt")
```

Ye file ko open karta hai.

```python
file.read()
```

Ye file ke andar ka **poora text read** karta hai.

```python
with
```

`with` use karne ka benefit ye hai ke Python kaam complete hone ke baad file ko automatically close kar deta hai.

---

## 4️⃣ Writing to a File

File ke andar data write karne ke liye `"w"` mode use hota hai.

```python
with open("my_file.txt", mode="w") as file:
    file.write("Hello Python!")
```

### Important:

`"w"` ka matlab **write mode** hai.

Agar file already exist karti ho, to `"w"` mode uska purana content replace kar sakta hai.

---

## 5️⃣ File Paths

Files ko access karte waqt hum path provide kar sakte hain.

Example:

```python
with open("Input/Names/invited_names.txt") as file:
    names = file.readlines()
```

Yahan:

```text
Input/
   └── Names/
        └── invited_names.txt
```

Python ko bataya gaya ke file kis folder ke andar located hai.

---

# 📬 Mail Merge Project

## 6️⃣ Mail Merge ka Concept

Mail Merge ka simple idea ye hai:

Ek hi letter ko multiple people ke liye personalize karna.

For example template:

```text
Dear [name],

You are invited to my birthday party!

Best wishes,
Shine
```

Agar names ki list ho:

```text
Alex
Ben
Charlie
David
```

To Python automatically separate letters create karega:

```text
Dear Alex,

You are invited to my birthday party!
```

```text
Dear Ben,

You are invited to my birthday party!
```

```text
Dear Charlie,

You are invited to my birthday party!
```

Is tarah manually har letter create karne ki zaroorat nahi padti.

---

## 7️⃣ Names File

`invited_names.txt` mein names store kiye:

```text
Alex
Ben
Charlie
David
Eleanor
Frank
```

Python in names ko read karega aur har name ke liye ek personalized letter banayega.

---

## 8️⃣ Letter Template

`starting_letter.txt` mein ek template letter rakha:

```text
Dear [name],

You are invited to my birthday party!

I hope you can make it.

Best wishes,
Shine
```

Yahan:

```text
[name]
```

ek **placeholder** hai.

Python is placeholder ko actual person's name se replace karega.

---

## 9️⃣ Reading Names

Names file ko read karne ke liye:

```python
with open("./Input/Names/invited_names.txt") as file:
    names = file.readlines()
```

`readlines()` file ki har line ko list ke ek element mein store karta hai.

For example:

```text
Alex
Ben
Charlie
```

ban jayega:

```python
["Alex\n", "Ben\n", "Charlie\n"]
```

Yahan `\n` ka matlab **new line** hai.

---

## 🔟 Reading the Letter Template

```python
with open("./Input/Letters/starting_letter.txt") as letter_file:
    letter_contents = letter_file.read()
```

Yahan:

```python
letter_contents
```

ke andar poora template letter store ho jata hai.

---

## 1️⃣1️⃣ Replacing the Name

Ab `[name]` ko actual name se replace karte hain:

```python
for name in names:
    stripped_name = name.strip()

    new_letter = letter_contents.replace("[name]", stripped_name)
```

### Explanation:

### `for name in names`

Names ki list mein se ek ek name leta hai.

### `strip()`

```python
name.strip()
```

Name ke beginning aur ending se extra spaces aur `\n` remove karta hai.

Example:

```python
"Alex\n"
```

becomes:

```python
"Alex"
```

### `replace()`

```python
letter_contents.replace("[name]", stripped_name)
```

Template ke andar:

```text
[name]
```

ko actual name se replace kar deta hai.

---

## 1️⃣2️⃣ Creating Personalized Letters

Ab har person ke liye separate file create kar sakte hain:

```python
for name in names:
    stripped_name = name.strip()

    new_letter = letter_contents.replace("[name]", stripped_name)

    with open(
        f"./Output/ReadyToSend/letter_for_{stripped_name}.txt",
        mode="w"
    ) as completed_letter:
        completed_letter.write(new_letter)
```

Agar name:

```text
Alex
```

hai to file banegi:

```text
letter_for_Alex.txt
```

Aur agar:

```text
Ben
```

hai to:

```text
letter_for_Ben.txt
```

---

# 1️⃣3️⃣ Complete `main.py`

```python
PLACEHOLDER = "[name]"

with open("./Input/Names/invited_names.txt") as names_file:
    names = names_file.readlines()

with open("./Input/Letters/starting_letter.txt") as letter_file:
    letter_contents = letter_file.read()

for name in names:
    stripped_name = name.strip()

    new_letter = letter_contents.replace(PLACEHOLDER, stripped_name)

    with open(
        f"./Output/ReadyToSend/letter_for_{stripped_name}.txt",
        mode="w"
    ) as completed_letter:
        completed_letter.write(new_letter)
```

---

## 1️⃣4️⃣ Program ka Flow

Program basically ye steps perform karta hai:

```text
Names File
    ↓
Names Read Karo
    ↓
Letter Template Read Karo
    ↓
Ek Ek Name Lo
    ↓
[name] ko Actual Name se Replace Karo
    ↓
New Letter Create Karo
    ↓
Output Folder Mein Save Karo
```

Example:

```text
invited_names.txt
       ↓
   ["Alex", "Ben", "Charlie"]
       ↓
starting_letter.txt
       ↓
"Dear [name], ..."
       ↓
[name] → Alex
[name] → Ben
[name] → Charlie
       ↓
Personalized Letters
```

---

## 1️⃣5️⃣ Important Python Concepts

### 📄 `open()`

File ko open karne ke liye:

```python
open("file.txt")
```

### 📖 `read()`

Poora file content read karta hai:

```python
file.read()
```

### 📚 `readlines()`

Har line ko list ke element ke taur par return karta hai:

```python
file.readlines()
```

### ✍️ `write()`

File mein data write karta hai:

```python
file.write("Hello")
```

### 🔄 `replace()`

Text replace karta hai:

```python
text.replace("[name]", "Alex")
```

### 🧹 `strip()`

Extra whitespace aur newline remove karta hai:

```python
name.strip()
```

### 🗂️ `with`

File ko safely handle karta hai:

```python
with open("file.txt") as file:
    data = file.read()
```

---

## 📸 Screenshot

<img width="1200" height="724" alt="1" src="https://github.com/user-attachments/assets/81dbba33-28ef-47ee-84c8-735a9ac3171d" />

---

## ✅ Key Takeaways

* Python se **local files ko read aur write** karna seekha
* `open()` function ko practically use kiya
* `read()` aur `readlines()` ka difference samjha
* `"w"` write mode use karna seekha
* Files aur folders ke **paths** handle kiye
* `strip()` se unwanted newline remove ki
* `replace()` se template ko personalize kiya
* `for` loop ke through multiple files automatically generate ki
* **Mail Merge** ke through Python ki basic automation practically implement ki
* File handling ko ek real-world use case ke sath connect kiya

---

## 🚀 Practice Ideas

* 📧 Multiple email templates generate karo
* 🎂 Birthday invitation generator banao
* 🏆 Students ke certificates automatically generate karo
* 📄 Names aur marks ki file se personalized result letters banao
* 📝 Ek template mein multiple placeholders use karo, jaise `[name]`, `[course]`, `[date]`
* 📁 Python ke through automatically folders create karne ki practice karo

---

## 🎯 Day 24 Summary

**Day 24 ka main lesson:**

> Python sirf calculations aur logic ke liye nahi hai — Python files aur folders ke sath kaam karke repetitive tasks ko automatically perform bhi kar sakta hai.

**Main concepts:**

```text
Files
 ↓
Directories
 ↓
File Paths
 ↓
Read / Write
 ↓
String Manipulation
 ↓
Automation
 ↓
Mail Merge Project
```
