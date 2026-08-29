# Day 93 — Personal Portfolio Project: PyPI Package Info Scraper

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Web Scraping a Live PyPI Package Page

A command-line tool that scrapes a real, live PyPI package page (e.g. `pypi.org/project/flask/`) using **`requests` + `BeautifulSoup`** — no API involved, pure HTML parsing. Extracts version, summary, license, Python requirement, and owner/maintainer. Built and debugged against real live pages, including two real bugs found and fixed during testing (see "Tested Output" below).

---

## 🧠 Concepts Covered

### 1. Fetching a real webpage's HTML
```python
import requests
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 ..."})
```
A `User-Agent` header is included because many sites block requests that look like a plain script (the default `requests` user-agent is an easy bot signal) — identifying as a browser reduces (but doesn't eliminate) the chance of being blocked.

### 2. Parsing HTML with BeautifulSoup
```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

name_header = soup.find("h1", class_="project-header__name")
```
`find()` locates the *first* matching tag; `find_all()` returns every match. Targeting a specific `class_` is what makes scraping reliable — matching by tag name alone (`<h1>`) would grab unrelated headings too.

### 3. Finding real CSS selectors by inspecting live HTML
The selectors used here weren't guessed — they were found by fetching the real page and printing its actual structure during development:
```python
for h1 in soup.find_all("h1"):
    print(h1.get("class"), h1.text.strip())
```
This is the actual first step of any real scraping project: the target site's HTML structure is unknown until you look at it directly, since it can differ from what you'd assume.

### 4. Extracting nearby but unlabeled content with `find_next()`
```python
summary_elem = name_header.find_next("p")
```
The package's tagline isn't in a conveniently-named element — it's just "the next `<p>` tag after the heading." `find_next()` searches forward from a known element instead of requiring every piece of content to have a unique class name.

### 5. Handling inconsistent page structure across different entries
**Real bug found during testing:** the `requests` package page didn't have the same "Owner" sidebar section that the `flask` page had — it only listed an "Author" in a different section.
```python
elif parts[0] == "Credits":
    if "Author:" in parts:
        idx = parts.index("Author:")
        if idx + 1 < len(parts) and owner == "Unknown":
            owner = parts[idx + 1]
```
Scraped pages are rarely as uniform as an API response — the same *kind* of page can lay out information differently depending on what data the source has. Always test against multiple real pages, not just one.

### 6. Detecting anti-bot challenge pages (not just HTTP errors)
**Second real bug found during testing:** requesting a nonexistent package didn't return a clean `404` — it returned `200` with an anti-bot **"Client Challenge"** page instead.
```python
page_title = soup.title.text.strip() if soup.title else ""
if "challenge" in page_title.lower() or "just a moment" in page_title.lower():
    print("⚠️  Blocked by an anti-bot challenge page...")
    return None
```
A `200` status code does **not** guarantee you received the content you expected — checking the actual page title/content caught a failure that status-code checking alone would have missed silently.

### 7. Being a respectful scraper
```python
import time
time.sleep(4)   # between requests, when scraping multiple pages
```
Sending requests too quickly is exactly what triggered the anti-bot challenge above during testing — spacing out requests is both more polite to the target server and less likely to get blocked.

---

## 📂 Project Structure
```
day93/
└── pypi_scraper.py
```

## ▶️ How to Run
```bash
pip install requests beautifulsoup4
python pypi_scraper.py flask
python pypi_scraper.py django
python pypi_scraper.py some-package-name
```

---

## 🧪 Tested Output — real, live scrapes

**Flask (real live data):**
```
=======================================================
  PyPI Package Report — Flask 3.1.3
=======================================================

📝 Summary:          A simple framework for building complex web applications.
⚖️  License:          BSD-3-Clause
🐍 Requires Python:   >=3.9
👤 Owner:             Pallets Projects
🛠️  Maintainer:        Pallets
🔗 URL:               https://pypi.org/project/flask/
```

**Django (real live data — confirms it works across different packages):**
```
Package        License             Requires Python     Owner
---------------------------------------------------------------------------
flask          BSD-3-Clause        >=3.9               Pallets Projects
django         BSD-3-Clause        >=3.12              Django Software Foundation
```

**Two real bugs found and fixed while testing against live pages:**
1. `requests` package page had no "Owner" section (unlike `flask`) — fixed by adding an "Author:" fallback from the Credits section. Verified afterward: correctly returned `Kenneth Reitz`.
2. Scraping a nonexistent package returned HTTP `200` with a "Client Challenge" anti-bot page instead of a clean `404` — fixed by checking the page `<title>` for challenge-page indicators. Verified afterward: script now prints a clear warning instead of returning garbage "Unknown" data.

---

## ✅ Key Takeaways
- Web scraping requires inspecting the *actual* live HTML first — selectors are found by exploring the real page, never guessed or assumed from memory.
- `find_next()` is essential when content you need isn't wrapped in a conveniently unique tag/class.
- Different pages of the "same kind" (e.g. two package pages) can have inconsistent structure — code should handle missing sections gracefully, not assume every page looks identical.
- **HTTP 200 does not mean you got the real content** — anti-bot challenge pages are a genuine scraping obstacle that status-code checking alone won't catch; checking the actual page title/content closed this gap.
- Spacing out requests (`time.sleep()`) is both more respectful to the target server and reduces the chance of triggering anti-bot protection — this was observed directly during testing, not just a theoretical concern.

## 📝 Practice Tasks
1. Extend the scraper to also pull the release date and file size of the latest release.
2. Add retry logic with exponential backoff for when a challenge page is hit, instead of just giving up.
3. Save scraped results to a CSV file so multiple packages can be compared later without re-scraping.
4. Compare this HTML-scraping approach to Day 91's GitHub API approach — which is more reliable, and why would a real project prefer an API when one is available?
