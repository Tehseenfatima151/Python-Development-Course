# Day 33 – Working with APIs & ISS Overhead Notifier Project

## 📌 Overview
Is session mein humne **APIs (Application Programming Interfaces)** ke sath kaam karna seekha — Python se internet se **live data** kaise fetch karte hain `requests` module ke through. Iske baad humne ye concept use kar ke **ISS Overhead Notifier** banaya — ek program jo check karta hai ke International Space Station (ISS) is waqt tumhare upar se guzar raha hai ya nahi, aur agar bahar andhera bhi ho, to tumhe email se alert bhej deta hai.

---

## 1️⃣ What is an API?

**API** ek "waiter" ki tarah hota hai — tum (client) usse request karte ho, wo backend (server) se data le kar tumhe wapis deta hai. Websites, apps, aur services (jaise weather, space data, currency rates) apna data **APIs ke through** publicly available karti hain.

```
Your Python Code  →  Request  →  API Server
Your Python Code  ←  Response (Data)  ←  API Server
```

---

## 2️⃣ The `requests` Module

Python ka `requests` library APIs se data fetch karne ka standard tareeqa hai.

```python
import requests

response = requests.get("https://api.example.com/data")
print(response.status_code)   # 200 = success, 404 = not found, waghera
print(response.text)           # Raw response (usually JSON string)
```

**Explanation:**
- `requests.get(url)` — us URL pe **GET request** bhejta hai (data mangna)
- `response.status_code` — batata hai request successful hui ya nahi (`200` = OK)
- **Status codes yaad rakhne wali baat:** `2xx` = success, `4xx` = client ki galti, `5xx` = server ki galti

### Checking for Errors

```python
response = requests.get("https://api.example.com/data")
response.raise_for_status()   # Agar error status ho (4xx/5xx), to exception raise karega
```

**Explanation:** `raise_for_status()` — agar request fail hui ho, to Python turant error de deta hai (bina isse, code silently galat data ke sath aage chal sakta hai).

---

## 3️⃣ Working with JSON Responses

Zyada tar APIs data **JSON** format mein deti hain — Python dictionaries jaisa lagta hai.

```python
response = requests.get("https://api.example.com/data")
data = response.json()

print(data["key"])
```

**Explanation:** `.json()` method response ko automatically Python dictionary/list mein parse kar deta hai — is se hum usse normal dictionary ki tarah access kar sakte hain.

---

## 4️⃣ Query Parameters (API Ko Specific Request Dena)

```python
parameters = {
    "lat": 24.8607,
    "lon": 67.0011,
}

response = requests.get("https://api.example.com/weather", params=parameters)
```

**Explanation:** `params=parameters` — dictionary automatically URL mein `?lat=24.8607&lon=67.0011` ki tarah convert ho jati hai. Ye manually string banane se kaafi cleaner tareeqa hai.

---

## 5️⃣ Building the ISS Overhead Notifier

**Concept:** ISS (International Space Station) Earth ke around ghoomta rehta hai. Ye project 2 conditions check karta hai:
1. **ISS abhi tumhare upar (5° ke andar) hai ya nahi**
2. **Abhi bahar andhera hai ya nahi** (kyunke andhere mein hi ISS naked-eye se dikh sakta hai)

Agar dono True hon, to email alert bhej dete hain.

### Step 1: ISS Ki Current Position Nikalna

```python
import requests

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])
```

**Explanation:** Ye API (`open-notify.org`) ISS ki current latitude/longitude return karta hai — nested JSON hai, is liye `data["iss_position"]["latitude"]` se access karte hain.

### Step 2: Apni Location Ke Coordinates

```python
MY_LAT = 24.8607   # Apni latitude yahan daalo
MY_LONG = 67.0011  # Apni longitude yahan daalo
```

### Step 3: Check Karna ISS Overhead Hai Ya Nahi

```python
iss_is_close = MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5
```

**Explanation:** Ye check karta hai ke ISS ki latitude/longitude tumhari location ke **±5 degree range** ke andar hai ya nahi — Python mein multiple comparisons ek line mein chain ki ja sakti hain (`a <= b <= c`).

### Step 4: Sunrise/Sunset API Se Andhera Check Karna

```python
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()

sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
```

**Explanation:**
- Response mein sunrise/sunset ek ISO format string mein hoti hai (jaise `"2026-08-04T18:32:00+00:00"`)
- `.split("T")[1]` — date aur time ko `T` se alag karta hai, time wala hissa leta hai
- `.split(":")[0]` — time se sirf hour nikalta hai

### Step 5 & 6: Current Time Nikal Kar Andhera Check Karna

```python
from datetime import datetime

time_now = datetime.now().hour
is_dark = time_now >= sunset or time_now <= sunrise
```

**Explanation:** Agar current hour sunset se baad ho, ya sunrise se pehle ho, to matlab bahar andhera hai.

### Step 7: Dono Conditions True Hon To Email Bhejna

```python
import smtplib

if iss_is_close and is_dark:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Subject:Look Up!\n\nThe ISS is above you in the sky right now!"
        )
```

---

## 6️⃣ Full Combined Program (Continuous Checking)

```python
import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 24.8607
MY_LONG = 67.0011
my_email = "your_email@gmail.com"
my_password = "your_app_password"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    return MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5


def is_night():
    parameters = {"lat": MY_LAT, "lng": MY_LONG, "formatted": 0}
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    return time_now >= sunset or time_now <= sunrise


def send_alert():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Subject:Look Up!\n\nThe ISS is above you in the sky right now!"
        )


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        send_alert()
```

**Explanation:** `while True` + `time.sleep(60)` — script har minute dono conditions check karta rehta hai, taake asal mein ISS overhead hote hi (aur andhera ho) turant alert mil jaye.
## Screenshoot
<img width="1166" height="720" alt="2" src="https://github.com/user-attachments/assets/c1709d25-36a3-4242-9d54-e4f512a28cda" />

---

## ✅ Key Takeaways
- APIs se live internet data lena `requests.get()` se hota hai — response `.json()` se Python dictionary mein convert hoti hai
- `raise_for_status()` se error responses ko silently ignore hone se bachate hain
- `params=` dictionary se query parameters cleanly URL mein add hote hain
- Multiple comparisons ek line mein chain ki ja sakti hain: `a <= b <= c`
- Ye project bohot saare pichle concepts combine karta hai: `requests` (naya), `datetime` (Day 32), `smtplib` (Day 32), string splitting, aur boolean logic
- `while True` + `time.sleep()` se koi bhi script "continuously monitor karta rehta hai" jaisa behavior mil jata hai

---

## 🔗 Practice Task
- Ek Weather Alert app banao jo `openweathermap.org` API use kar ke rain-alert email bheje
- ISS Notifier mein current ISS location ko map pe Turtle se plot karo
- Error handling add karo — agar API down ho ya internet na ho, to program crash na ho, friendly message de
