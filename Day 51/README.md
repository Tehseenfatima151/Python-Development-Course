# Day 51 – Selenium WebDriver & Twitter Complaint Bot

## 📌 Overview
Is session mein humne **Selenium WebDriver** seekha — ek powerful tool jo Python se **real browser ko automate** karta hai. Iske baad humne ek **Twitter Complaint Bot** banaya — jo automatically browser khol kar Twitter (X) pe login karta hai aur ek pre-written complaint tweet post kar deta hai.

---

## 1️⃣ BeautifulSoup vs Selenium — Farq Kya Hai?

| BeautifulSoup (Day 45) | Selenium |
|--------------------------|----------|
| Sirf static HTML parhta hai | Real browser khol kar interact karta hai |
| Click/type/scroll nahi kar sakta | Click, type, scroll, sab kar sakta hai |
| JavaScript-generated content nahi dikhta | JavaScript-rendered content bhi dikhta hai |
| Fast, lightweight | Thora slow, lekin zyada powerful |

**Explanation:** Jab website JavaScript se dynamically content load karti hai (jaise Twitter), ya jab login/click/form-fill karna ho, to Selenium chahiye hota hai.

---

## 2️⃣ Setting Up Selenium

```bash
pip install selenium
```

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.google.com")
```

**Explanation:**
- `webdriver.Chrome()` — Chrome browser ka ek naya, controllable instance launch karta hai
- `driver.get(url)` — us URL pe navigate karta hai

---

## 3️⃣ Finding Elements on the Page

```python
driver.find_element(by="id", value="search-box")
driver.find_element(by="name", value="username")
driver.find_element(by="css selector", value=".login-button")
driver.find_element(by="xpath", value="//button[@type='submit']")
```

**Explanation:**
- `by="id"` — sabse reliable
- `by="css selector"` — CSS syntax use karta hai
- `by="xpath"` — sabse flexible/powerful

---

## 4️⃣ Interacting with Elements

```python
search_box = driver.find_element(by="name", value="q")
search_box.send_keys("Python programming")
search_box.submit()

button = driver.find_element(by="id", value="submit-btn")
button.click()
```

**Explanation:**
- `.send_keys("text")` — jaise keyboard se type karna
- `.click()` — mouse click simulate karna
- `.submit()` — form submit karna

---

## 5️⃣ Waiting for Elements

```python
import time
time.sleep(3)   # Simple lekin unreliable wait
```

Better approach — Explicit Wait:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "search-box")))
```

**Explanation:** `WebDriverWait` element ke available hone tak wait karta hai — `time.sleep()` se zyada efficient aur reliable.

---

## 6️⃣ Building the Twitter Complaint Bot

**Concept:** Bot automatically browser khol kar Twitter (X) pe login karta hai, tweet-box mein ek pre-written complaint likh kar post kar deta hai.

⚠️ **Important:** Ye project sirf educational purpose ke liye hai — automated posting kisi bhi platform ki Terms of Service ke against ho sakti hai, responsibly aur apne khud ke account pe hi test karo.

### Step 1: Environment Variables (Day 35 Wala Concept)

```python
import os
from dotenv import load_dotenv

load_dotenv()

TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")
```

### Step 2-4: Browser Launch, Login

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://twitter.com/login")
time.sleep(3)

email_field = driver.find_element(By.NAME, "text")
email_field.send_keys(TWITTER_EMAIL)
email_field.submit()
time.sleep(2)

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys(TWITTER_PASSWORD)
password_field.submit()
time.sleep(3)
```

### Step 5-6: Tweet Compose Karna aur Post Karna

```python
tweet_box = driver.find_element(By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']")
tweet_box.click()

complaint_text = "Hey @Airline, my flight was delayed 3 hours with zero communication. #CustomerService"
tweet_box.send_keys(complaint_text)
time.sleep(1)

tweet_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='tweetButton']")
tweet_button.click()
time.sleep(2)

driver.quit()
```

**Explanation:** `driver.quit()` browser session ko band kar deta hai — hamesha script ke end mein call karo taake resources free ho jayein.

---

## 7️⃣ Full Combined Program

```python
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv()

TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")
COMPLAINT_TEXT = "Hey @Airline, my flight was delayed 3 hours with zero communication. #CustomerService"


def post_complaint_tweet():
    driver = webdriver.Chrome()
    driver.get("https://twitter.com/login")
    time.sleep(3)

    email_field = driver.find_element(By.NAME, "text")
    email_field.send_keys(TWITTER_EMAIL)
    email_field.submit()
    time.sleep(2)

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(TWITTER_PASSWORD)
    password_field.submit()
    time.sleep(3)

    tweet_box = driver.find_element(By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']")
    tweet_box.click()
    tweet_box.send_keys(COMPLAINT_TEXT)
    time.sleep(1)

    tweet_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='tweetButton']")
    tweet_button.click()
    time.sleep(2)

    print("Complaint tweet posted successfully!")
    driver.quit()


if __name__ == "__main__":
    post_complaint_tweet()
```

---

## ✅ Key Takeaways
- Selenium real browser ko automate karta hai — clicking, typing, form-filling sab kar sakta hai, BeautifulSoup se zyada powerful
- `find_element(by=..., value=...)` se different strategies (ID, class, CSS selector, XPath) se elements dhoondte hain
- `.send_keys()` type karta hai, `.click()` click karta hai, `.submit()` form submit karta hai
- Fixed `time.sleep()` unreliable hai — `WebDriverWait` + `expected_conditions` zyada robust approach hai
- Login credentials hamesha `.env` file se load karo, kabhi hardcode nahi (Day 35 principle)
- `driver.quit()` script ke end mein call karna zaroori hai
- Automation scripts jo social media platforms interact karti hain, unhe responsibly aur ethically use karna chahiye

---

## 🔗 Practice Task
- Bot ko modify karo taake wo multiple complaints (ek list se) automatically post kare, delay ke sath
- `WebDriverWait` implement karo fixed `time.sleep()` ki jagah
- Ek "confirmation" step add karo — tweet post karne se pehle user se terminal mein confirm karwao

---

## 📸 Screenshot
<img width="1338" height="717" alt="image" src="https://github.com/user-attachments/assets/a28dcafc-1c5f-4108-a3ac-33fa3f9f0557" />

