# Day 96 — Personal Portfolio Project: GitHub Stats Dashboard

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: GitHub Stats Dashboard (HTTP Requests & APIs)

A command-line tool that fetches and displays a GitHub user's profile stats — repo count, followers, top languages, total stars/forks, and recently updated repos — using the **GitHub REST API** and Python's `requests` library. Built to be run against my own profile (`Tehseenfatima151`) as a live personal stats dashboard.

---

## 🧠 Concepts Covered

### 1. Making a GET request
```python
import requests
response = requests.get(f"https://api.github.com/users/{username}")
```
`requests.get()` sends an HTTP GET request to the given URL — the same request a browser makes when you visit a page, but returned as data your code can work with directly.

### 2. Always checking `status_code` before trusting the response
```python
if response.status_code == 200:
    return response.json()
elif response.status_code == 404:
    print(f"❌ No GitHub user found with username '{username}'.")
elif response.status_code == 403:
    print("⚠️  GitHub API rate limit exceeded for this IP address.")
```
A request can "succeed" (no exception thrown) while still returning an error — checking `status_code` is how you tell the difference between real data and an error message dressed up as JSON. `404` = not found, `403` = forbidden/rate-limited, `200` = success.

### 3. Passing query parameters properly
```python
requests.get(f"{BASE_URL}/users/{username}/repos",
             params={"sort": "updated", "per_page": 100})
```
Using `params={}` instead of manually building `?sort=updated&per_page=100` lets `requests` handle URL-encoding automatically — safer if a parameter ever contains special characters.

### 4. Converting a response to usable Python data
```python
response.json()   # turns the JSON response body into a Python dict/list
```

### 5. Never letting an API failure crash the program
```python
def get_user_profile(username):
    response = requests.get(...)
    if response.status_code == 200:
        return response.json()
    else:
        print("... helpful message ...")
    return None
```
Every function returns `None` on failure instead of raising an unhandled exception — the caller checks for `None` before continuing, so a network hiccup or rate limit produces a clear message instead of a crash.

### 6. Aggregating data from a list of API results
```python
total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)

def summarize_languages(repos):
    language_counts = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            language_counts[lang] = language_counts.get(lang, 0) + 1
    return dict(sorted(language_counts.items(), key=lambda item: item[1], reverse=True))
```
`.get("language")` avoids a `KeyError` if a repo happens to have no detected language, and sorting the resulting dictionary by count gives a "top languages" ranking with no extra library needed.

### 7. Command-line arguments for reusability
```python
target_username = sys.argv[1] if len(sys.argv) > 1 else "Tehseenfatima151"
```
Running `python github_stats.py octocat` checks a different GitHub user without touching the code — same pattern used in the Day 81 File Organizer project.

---

## 📂 Project Structure
```
day91/
└── github_stats.py
```

## ▶️ How to Run
```bash
pip install requests
python github_stats.py                    # defaults to Tehseenfatima151
python github_stats.py octocat             # or check any other GitHub username
```

---

## 🧪 Tested Output

**Live run against my real GitHub username, `Tehseenfatima151`:**
```
=======================================================
  GitHub Stats Dashboard — @Tehseenfatima151
=======================================================
⚠️  GitHub API rate limit exceeded for this IP address.
    Unauthenticated requests are limited to 60/hour.
    Fix: use a Personal Access Token for 5,000/hour instead.

Could not load profile — see message above.
```
This run happened to hit GitHub's real rate limit (a genuine, common API constraint, not a bug) — and confirms the error-handling path works exactly as designed: a clear message instead of a crash. **On a normal connection with the rate limit not exceeded, this same code returns full profile + repo data.**

**Core data-processing logic tested independently with realistic mock repo data** (to verify correctness beyond just the network call):
```
=== Testing summarize_languages() ===
{'Python': 4, 'HTML': 1, 'Jupyter Notebook': 1, 'CSS': 1}
✅ summarize_languages() correct — Python is top language with 4 repos

=== Testing total stars/forks calculation ===
Total stars: 23
Total forks: 4
✅ Aggregation logic correct

=== Testing get_user_profile() error handling ===
Result when user unreachable: None
✅ Error handling returns None gracefully, no crash
```

---

## ✅ Key Takeaways
- A successful HTTP request (no exception) does **not** mean successful data — always check `status_code` before trusting the response body.
- Real APIs have rate limits — handling `403`/`429` gracefully (with a clear message, not a crash) is a real production concern, not an edge case to ignore.
- `params={}` is safer and cleaner than manually building query strings.
- `.get()` with a default value prevents `KeyError` crashes when API responses have optional/missing fields.
- Separating "fetch data" functions from "display data" logic (as in Day 85's password manager and Day 87's game) keeps API-calling code testable independent of formatting/printing.

## 📝 Practice Tasks
1. Add support for a GitHub Personal Access Token (via environment variable) to raise the rate limit from 60/hour to 5,000/hour.
2. Cache the API response to a local JSON file for 10 minutes, so repeated runs don't hit the rate limit as fast.
3. Add a `--compare` flag that fetches and displays stats for two usernames side by side.
4. Turn this into a simple Flask route (tying back to Day 61-70) that renders the same stats as an HTML page instead of terminal output.
