# Day 25 – Working with CSV Files, Data Analysis with Pandas & US States Game

## 📌 Overview
Is session mein humne **CSV files** ke sath kaam karna seekha aur **pandas** library se data analysis kiya — ye Python ki sabse popular data science library hai. Iske baad humne ye concepts use kar ke **US States Game** banaya — ek quiz jahan user US map pe states ke naam guess karta hai, aur missed states ek nayi CSV file mein save ho jate hain.

---

## 1️⃣ What is CSV?

**CSV (Comma-Separated Values)** ek simple text file format hai jisme data **tabular** (rows aur columns) form mein store hota hai — bilkul Excel spreadsheet jaisa, bas plain text mein.

```
name,age,city
Ali,22,Lahore
Sara,21,Karachi
Ahmed,23,Islamabad
```

Har line ek **row** hai, comma se **columns** separate hote hain.

---

## 2️⃣ Reading CSV — Without Pandas (Basic Way)

```python
import csv

with open("data.csv") as file:
    data = csv.reader(file)
    for row in data:
        print(row)
```

**Explanation:** Python ka built-in `csv` module file ko row-by-row read karta hai — har row ek list ki soorat mein milta hai. Ye kaam karta hai, lekin bare datasets ke liye inconvenient hai.

---

## 3️⃣ What is Pandas?

**Pandas** ek powerful Python library hai jo data ko **DataFrame** (table jaisi structure) mein load kar deti hai, jisse filtering, sorting, calculations, aur analysis bohot aasan ho jata hai.

```python
import pandas as pd

data = pd.read_csv("data.csv")
print(data)
```

**Explanation:** `pd.read_csv()` poori CSV file ko ek **DataFrame** object mein load kar deta hai — Excel jaisi table, jisme rows aur columns hote hain, aur bohot saare built-in methods available hote hain.

---

## 4️⃣ Exploring a DataFrame

```python
data = pd.read_csv("data.csv")

print(data.head())        # Pehli 5 rows dikhata hai
print(data.info())        # Columns, data types, aur missing values ka summary
print(data.columns)       # Sare column names
print(data["name"])       # Sirf "name" column nikalta hai (ye ek "Series" hai)
```

---

## 5️⃣ Filtering Data with Pandas

```python
# Sirf wo rows jinki age 22 se zyada hai
older_than_22 = data[data.age > 22]
print(older_than_22)

# Specific value dhoondhna
lahore_people = data[data.city == "Lahore"]
```

**Explanation:** `data.age > 22` ek **boolean mask** banata hai (True/False ki list), aur `data[mask]` sirf True wali rows return karta hai — ye pandas ka sabse powerful feature hai.

---

## 6️⃣ Converting Rows/Columns to Lists

```python
names_list = data["name"].to_list()
print(names_list)   # ['Ali', 'Sara', 'Ahmed']
```

**Explanation:** `.to_list()` ek pandas column (Series) ko normal Python list mein convert kar deta hai — is se hum usse loops, comparisons, waghera mein easily use kar sakte hain.

---

## 7️⃣ Writing Data to a New CSV

```python
new_data = pd.DataFrame({
    "name": ["Ali", "Sara"],
    "score": [85, 92]
})

new_data.to_csv("results.csv", index=False)
```

**Explanation:** `index=False` isliye zaroori hai warna pandas apna khud ka extra "index number" column bhi CSV mein likh deta hai, jo zaroori nahi hota.

---

## 8️⃣ Building the US States Game

**Concept:** Ek US map screen pe dikhta hai, user state ka naam type karta hai, aur agar sahi ho to us state ka naam map pe uski jagah likh diya jata hai. Jab user "Exit" type kare (ya sare 50 guess ho jayein), to jo states miss huay unki list ek nayi CSV file mein save ho jati hai.

### Step 1: Reading the States Data

```python
import pandas as pd
from turtle import Screen, Turtle

data = pd.read_csv("50_states.csv")
all_states = data.state.to_list()   # Sare 50 states ki list
```

**Explanation:** CSV file mein har state ka naam aur uski x/y coordinates hoti hain (map pe position ke liye).

### Step 2: Screen Setup

```python
screen = Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)

turtle = Turtle()
turtle.shape(image)
```

**Explanation:** `addshape()` se ek image (blank US map) ko turtle ka "shape" bana dete hain — ye background ki tarah use hoti hai.

### Step 3: Game Loop — Guessing States

```python
guessed_states = []

while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"{len(guessed_states)}/50 States Correct",
                                     prompt="What's another state's name?").title()

    if answer_state == "Exit":
        break

    if answer_state in all_states:
        guessed_states.append(answer_state)
        t = Turtle()
        t.hideturtle()
        t.penup()

        state_data = data[data.state == answer_state]
        t.goto(int(state_data.x.iloc[0]), int(state_data.y.iloc[0]))
        t.write(answer_state)
```

**Explanation:**
- `screen.textinput()` — popup dialog box khol kar user se naam leta hai
- `.title()` — string ko proper case mein convert karta hai (jaise "texas" → "Texas") taake comparison sahi ho
- `data[data.state == answer_state]` — pandas filtering se us state ki row dhoondte hain
- `.x.iloc[0]` — filtered result ka pehla (aur sirf) row ki `x` value nikalte hain
- `t.write(answer_state)` — state ka naam map pe uski sahi jagah likh deta hai

### Step 4: Missed States — CSV Mein Save Karna

```python
missing_states = [state for state in all_states if state not in guessed_states]

new_data = pd.DataFrame(missing_states)
new_data.to_csv("states_to_learn.csv")
```

**Explanation:**
- **List comprehension** se un states ki list banate hain jo `all_states` mein hain lekin `guessed_states` mein nahi (yani jo miss ho gaye)
- Ye list ek nayi CSV file mein save ho jati hai — is se user ko pata chal jata hai ke kaunse states usse practice karne hain

---

## 9️⃣ Full Combined Program

```python
import pandas as pd
from turtle import Screen, Turtle

data = pd.read_csv("50_states.csv")
all_states = data.state.to_list()

screen = Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)

turtle = Turtle()
turtle.shape(image)

guessed_states = []

while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"{len(guessed_states)}/50 States Correct",
                                     prompt="What's another state's name? Type 'Exit' to quit.").title()

    if answer_state == "Exit":
        missing_states = [state for state in all_states if state not in guessed_states]
        new_data = pd.DataFrame(missing_states)
        new_data.to_csv("states_to_learn.csv")
        break

    if answer_state in all_states:
        guessed_states.append(answer_state)
        t = Turtle()
        t.hideturtle()
        t.penup()

        state_data = data[data.state == answer_state]
        t.goto(int(state_data.x.iloc[0]), int(state_data.y.iloc[0]))
        t.write(answer_state)

screen.exitonclick()
```

---
## Screenshoot
<img width="713" height="644" alt="1" src="https://github.com/user-attachments/assets/61adb0e0-3160-4d4c-a177-b1f6f05cae5f" />


## ✅ Key Takeaways
- CSV files data ko simple, comma-separated tabular format mein store karti hain
- Pandas `read_csv()` se data ko powerful `DataFrame` structure mein load karta hai — filtering, analysis sab aasan ho jata hai
- Boolean filtering (`data[data.column > value]`) pandas ka core feature hai
- `.to_list()` se pandas column ko normal Python list mein convert karte hain
- `.to_csv()` se naya data file mein export karte hain
- US States Game real-world data analysis (pandas) aur Turtle graphics ka combined practical use hai — CSV se location data read karna aur user progress ko wapis CSV mein save karna

---

## 🔗 Practice Task
- Game khatam hone pe percentage score bhi show karo (kitne % states sahi guess huay)
- Ek "hint" feature add karo jo random ek missed state ka naam bata de
- CSV se sirf ek specific region (jaise "West Coast states") ki list filter kar ke practice mode banao
