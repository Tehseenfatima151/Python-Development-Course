# Day 32 – Email (SMTP), datetime Module & Birthday Wisher Project

## 📌 Overview
Is session mein humne Python se **automatically emails bhejna** seekha (`smtplib` module se) aur **`datetime` module** se current date/time ke sath kaam karna seekha. Iske baad humne ye dono concepts combine kar ke ek **Birthday Wisher** program banaya — jo roz check karta hai ke aaj kisi ka birthday hai ya nahi, aur agar ho to automatically ek random personalized wish email bhej deta hai.

---

## 1️⃣ The `datetime` Module

Python ka built-in module jo date aur time ke sath kaam karne deta hai.

```python
from datetime import datetime

now = datetime.now()
print(now)             # 2026-08-04 14:35:12.123456

print(now.year)         # 2026
print(now.month)        # 8
print(now.day)          # 4
print(now.weekday())    # 0 = Monday, 6 = Sunday
```

**Explanation:** `datetime.now()` current date aur time ka ek object return karta hai — usme se `.year`, `.month`, `.day` jaisi individual values nikali ja sakti hain.

### Formatting Dates

```python
formatted = now.strftime("%A, %d %B %Y")
print(formatted)   # "Tuesday, 04 August 2026"
```

**Explanation:** `strftime()` date ko readable string mein convert karta hai — `%A` = full weekday name, `%d` = day number, `%B` = full month name, `%Y` = 4-digit year.

---

## 2️⃣ Sending Emails with `smtplib`

**SMTP (Simple Mail Transfer Protocol)** wo standard hai jisse emails bheji jati hain. Python ka `smtplib` module isse implement karta hai.

```python
import smtplib

my_email = "your_email@gmail.com"
password = "your_app_password"

with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs="recipient@email.com",
        msg="Subject:Hello\n\nThis is the email body."
    )
```

**Explanation:**
- `smtplib.SMTP("smtp.gmail.com", port=587)` — Gmail ke SMTP server se connection banata hai (port 587 = TLS wala secure port)
- `connection.starttls()` — connection ko encrypt kar deta hai, taake password/data secure rahe
- `connection.login()` — apne email account mein login karta hai
- `connection.sendmail()` — asal email bhejta hai — `msg` mein `"Subject:...\n\n..."` format zaroori hai

### ⚠️ Important: Gmail "App Password"

Gmail apne normal password se scripts ko login nahi karne deta. Iske liye:
1. Google Account → Security → **2-Step Verification** enable karo
2. Phir **"App Passwords"** section mein jao
3. Ek naya 16-digit app password generate karo
4. Ye password apne script mein use karo (apna normal Gmail password nahi)

---

## 3️⃣ Reading Multiple Recipients (Pandas Ke Sath — Day 25 Concept)

```python
import pandas as pd

data = pd.read_csv("birthdays.csv")

for (index, row) in data.iterrows():
    print(row["email"], row["name"])
```

---

## 4️⃣ Building the Birthday Wisher Project

**Concept:** Ek `birthdays.csv` file mein dosto ke naam, email, aur birth-date store hain. Program roz check karta hai — agar aaj kisi ka birthday hai, to usse ek random letter template se personalized wish email bhej deta hai.

### Project Structure

```
birthday_wisher/
├── main.py
├── birthdays.csv
└── letter_templates/
    ├── letter_1.txt
    ├── letter_2.txt
    └── letter_3.txt
```

### Step 1: `birthdays.csv`

```
name,email,year,month,day
Angela,angela@email.com,1990,8,4
Ali,ali@email.com,1998,8,4
Sara,sara@email.com,2000,12,15
```

### Step 2: Letter Templates (Placeholder Ke Sath)

`letter_1.txt`:
```
Dear [NAME],

Happy Birthday! I hope you have a fantastic day filled with joy.

Best wishes,
Your Friend
```

**Explanation:** `[NAME]` placeholder hai — bilkul Day 24 (Mail Merge) wala pattern.

### Step 3: Aaj Ki Date Nikalna aur Match Check Karna

```python
from datetime import datetime
import pandas as pd
import random
import smtplib

today = datetime.now()
today_tuple = (today.month, today.day)

data = pd.read_csv("birthdays.csv")
birthdays_dict = {(row.month, row.day): row for (index, row) in data.iterrows()}

if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
```

**Explanation:**
- `(today.month, today.day)` — ek tuple banate hain (Day 18 wala concept — fixed, comparable values ke liye tuples perfect hain)
- Dict comprehension (Day 26) se `{(month, day): person_row}` ka lookup dictionary banaya
- `if today_tuple in birthdays_dict` — check karta hai ke aaj ki date kisi ke birthday se match karti hai ya nahi

### Step 4: Random Letter Choose Karna aur Naam Replace Karna

```python
    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"

    with open(file_path) as letter_file:
        contents = letter_file.read()

    personalized_letter = contents.replace("[NAME]", birthday_person["name"])
```

**Explanation:** `random.randint(1, 3)` — 3 templates mein se ek randomly choose karta hai, taake har baar same message na jaye.

### Step 5: Email Bhejna

```python
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday!\n\n{personalized_letter}"
        )
```

---

## 5️⃣ Full Combined Program

```python
from datetime import datetime
import pandas as pd
import random
import smtplib

my_email = "your_email@gmail.com"
my_password = "your_app_password"

today = datetime.now()
today_tuple = (today.month, today.day)

data = pd.read_csv("birthdays.csv")
birthdays_dict = {(row.month, row.day): row for (index, row) in data.iterrows()}

if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]

    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()

    personalized_letter = contents.replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday!\n\n{personalized_letter}"
        )

    print(f"Birthday email sent to {birthday_person['name']}!")
else:
    print("No birthdays today.")
```

---

## 6️⃣ Automating It (Daily Run)

Ye script apne aap roz kaam kare, is ke liye **scheduler** use karte hain (Python ke bahar):
- **Windows** — Task Scheduler se roz ek fixed time pe script run karwa sakte ho
- **Mac/Linux** — `cron` job set kar sakte ho

```bash
# cron example: har din subah 9 baje script chalao
0 9 * * * python3 /path/to/main.py
```
## Screenshoot
<img width="1193" height="727" alt="1" src="https://github.com/user-attachments/assets/ac727ec1-d647-4fa0-8419-85006d8597df" />

---

## ✅ Key Takeaways
- `smtplib` se Python email bhej sakta hai — `starttls()` connection secure karta hai, `login()` authenticate karta hai
- Gmail ke sath script use karne ke liye **App Password** zaroori hai, normal password nahi chalega
- `datetime.now()` se current date/time milta hai, `.month`/`.day`/`.year` se individual parts
- Tuples (`(month, day)`) date comparison ke liye perfect hain — fixed, hashable, dictionary keys ban sakte hain
- Ye project Mail Merge (Day 24), pandas (Day 25), dict comprehension (Day 26), aur naya SMTP/datetime concept — sab ek sath use karta hai
- Real automation (scheduled scripts) Python code se bahar OS-level tools (`cron`, Task Scheduler) se hoti hai

---

## 🔗 Practice Task
- Program ko modify karo taake ye "Anniversary Wisher" bhi ban sake (dusri CSV, dusra event type)
- Email ke sath ek attachment (jaise ek greeting card image) bhejne ka logic add karo
- Error handling add karo — agar SMTP login fail ho jaye to friendly error message print ho, crash na ho
