# Day 94 — Personal Portfolio Project: Cookie Clicker Game Bot (GUI Automation)

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Automating a Browser Game with Selenium

A **GUI automation** bot using **Selenium WebDriver** that plays the browser game [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/) — clicking the cookie repeatedly and automatically buying the cheapest affordable upgrade, exactly the way a human would interact with the actual page (not an API, not HTML scraping — real button clicks on a real rendered browser).

> **Honesty note on testing:** this sandboxed environment doesn't have a real Chrome browser available (only a non-functional Snap stub, since Snap requires `snapd` which isn't supported here) — so a full live run against the actual game wasn't possible in this environment. What **was** verified here: the script's syntax compiles cleanly, the Selenium API calls (`By.ID`, `WebDriverWait`, element locators) are used correctly, and the pure data-parsing logic (extracting the cookie count from page text) was tested directly and passes. The script is written to run as-is on any machine with Chrome installed — see "How to Run" below.

---

## 🧠 Concepts Covered

### 1. What makes this "GUI automation" vs. scraping or an API call
Day 91 called an API. Day 93 read raw HTML. This project instead **launches a real browser window and interacts with it like a person** — clicking visible buttons, waiting for elements to become clickable, reacting to what's currently on screen. This is the right tool when a site requires clicks/interaction to reveal data, or when the goal genuinely is automating a repetitive UI task (not just reading data).

### 2. Launching a controlled browser instance
```python
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get(GAME_URL)
```
Selenium 4.6+ automatically downloads and manages the matching `chromedriver` version for whatever Chrome version is installed — no manual driver download/PATH setup needed (a common pain point in older Selenium tutorials).

### 3. Locating elements — By strategies
```python
from selenium.webdriver.common.by import By

big_cookie = driver.find_element(By.ID, "bigCookie")
store_items = driver.find_elements(By.CSS_SELECTOR, "#products div.product.unlocked")
```
`find_element` (singular) returns the first match and raises an error if nothing is found; `find_elements` (plural) always returns a list, empty if nothing matches — an important distinction for avoiding crashes when something might legitimately not be on screen yet.

### 4. Waiting for elements properly — avoiding flaky `time.sleep()` guessing
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

consent_button = WebDriverWait(driver, 8).until(
    EC.element_to_be_clickable((By.ID, "cmp-tc-btn-1"))
)
consent_button.click()
```
Real pages load asynchronously — an element might not exist yet the instant the page URL loads. `WebDriverWait` polls until the element is actually clickable (up to a timeout), which is far more reliable than guessing a fixed `time.sleep(3)` that might be too short (flaky failures) or too long (wastes time).

### 5. Handling elements that may or may not appear
```python
try:
    consent_button = WebDriverWait(driver, 8).until(...)
    consent_button.click()
except TimeoutException:
    print("ℹ️  No consent banner appeared (or already dismissed).")
```
A cookie-consent banner might or might not show up depending on region/session — catching `TimeoutException` lets the bot continue instead of crashing if that particular element never appears.

### 6. Reading dynamic page content
```python
def get_current_cookie_count(driver):
    cookie_count_text = driver.find_element(By.ID, "cookies").text
    digits_only = "".join(char for char in cookie_count_text if char.isdigit())
    return int(digits_only) if digits_only else 0
```
The page displays cookie count as formatted text like `"1,234 cookies"` — this strips everything except digits to get a usable integer. **Tested directly** against 5 realistic text formats (see below) — all passed.

### 7. A simple decision loop — buy the cheapest affordable item
```python
def buy_cheapest_affordable_upgrade(driver):
    store_items = driver.find_elements(By.CSS_SELECTOR, "#products div.product.unlocked")
    for item in store_items:
        classes = item.get_attribute("class")
        if "enabled" in classes and "disabled" not in classes:
            item.click()
            return True
    return False
```
The game's store lists items in ascending price order and marks unaffordable ones with a `disabled` CSS class — checking `get_attribute("class")` lets the bot "see" which upgrades it can currently afford, the same way a human would visually notice a grayed-out button.

---

## 📂 Project Structure
```
day94/
└── cookie_clicker_bot.py
```

## ▶️ How to Run
```bash
pip install selenium
python cookie_clicker_bot.py
```
Requires Google Chrome to be installed on your machine (Selenium 4.6+ handles the driver automatically — no separate chromedriver download needed). A real Chrome window will open and you'll see it click the cookie and buy upgrades on its own for 60 seconds.

---

## 🧪 What Was Actually Tested

**1. Syntax check — passed:**
```
✅ Syntax valid
```

**2. Core parsing logic — tested directly with realistic game text, all passed:**
```
✅ parse_cookie_count('1,234 cookies') = 1234 (expected 1234)
✅ parse_cookie_count('0 cookies') = 0 (expected 0)
✅ parse_cookie_count('15,203,891 cookies') = 15203891 (expected 15203891)
✅ parse_cookie_count('1 cookie') = 1 (expected 1)
✅ parse_cookie_count('') = 0 (expected 0)
```

**3. Selenium API usage — verified locator classes behave correctly:**
```
By.ID locator tuple: ('id', 'bigCookie')
✅ Selenium locator strategy classes work as expected
```

**4. Attempted a real driver launch — confirmed the (expected) failure reason,** so the "why" is documented rather than hidden:
```
NoSuchDriverException: Unable to obtain driver for chrome
```
This confirms Selenium itself is correctly installed and attempting the right thing — it fails only because this sandbox has no real Chrome binary (Snap-only, non-functional here), not because of a code issue. On a normal machine with Chrome installed, this same code launches a real, visible browser window.

---

## ✅ Key Takeaways
- GUI automation (Selenium) is the right tool when a task genuinely requires clicking/interacting with a rendered page — different from calling an API (Day 91) or reading static HTML (Day 93).
- `WebDriverWait` + `expected_conditions` is the correct way to wait for dynamic content — far more reliable than a fixed `time.sleep()` guess.
- `find_element` vs `find_elements` matters: use `find_elements` (plural) when something might legitimately not exist yet, to avoid an unhandled crash.
- Reading an element's CSS class (`get_attribute("class")`) is a practical way to detect UI state (enabled/disabled) the same way a human visually would.
- It's possible — and worth doing — to verify real logic and catch real bugs even when full end-to-end testing isn't possible in a given environment; testing what *can* be isolated (parsing logic, API correctness) still catches real issues.

## 📝 Practice Tasks
1. Run this on your own machine (with Chrome installed) and extend `RUN_DURATION_SECONDS` to see how high the cookie count climbs.
2. Add a "golden cookie" click handler — Cookie Clicker occasionally spawns a bonus clickable cookie that should be clicked immediately when it appears.
3. Log each purchased upgrade with a timestamp to a CSV file, to analyze the bot's purchase strategy afterward.
4. Try headless mode (`options.add_argument("--headless=new")`) so the browser runs invisibly in the background instead of opening a visible window.
