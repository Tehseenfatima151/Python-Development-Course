"""
Day 91 — Personal Portfolio Project: GitHub Stats Dashboard
Fetches and displays a GitHub user's profile stats and repository
data using the GitHub REST API and the `requests` library.

Run: python github_stats.py [username]
Defaults to "Tehseenfatima151" if no username is given.
"""

import requests
import sys

BASE_URL = "https://api.github.com"


def get_user_profile(username: str) -> dict | None:
    """Fetch a GitHub user's public profile data.
    Returns None (with a printed message) on any failure — never crashes."""
    response = requests.get(f"{BASE_URL}/users/{username}")

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print(f"❌ No GitHub user found with username '{username}'.")
    elif response.status_code == 403:
        print("⚠️  GitHub API rate limit exceeded for this IP address.")
        print("    Unauthenticated requests are limited to 60/hour.")
        print("    Fix: use a Personal Access Token for 5,000/hour instead.")
    else:
        print(f"⚠️  Unexpected error: {response.status_code} — {response.text[:150]}")

    return None


def get_user_repos(username: str, sort_by: str = "updated") -> list | None:
    """Fetch a GitHub user's public repositories, sorted by the given field."""
    response = requests.get(
        f"{BASE_URL}/users/{username}/repos",
        params={"sort": sort_by, "per_page": 100}
    )

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        print("⚠️  GitHub API rate limit exceeded — repos couldn't be fetched.")
    else:
        print(f"⚠️  Couldn't fetch repos: {response.status_code}")

    return None


def summarize_languages(repos: list) -> dict:
    """Count how many repos use each language."""
    language_counts = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            language_counts[lang] = language_counts.get(lang, 0) + 1
    return dict(sorted(language_counts.items(), key=lambda item: item[1], reverse=True))


def print_dashboard(username: str):
    print("=" * 55)
    print(f"  GitHub Stats Dashboard — @{username}")
    print("=" * 55)

    profile = get_user_profile(username)
    if profile is None:
        print("\nCould not load profile — see message above.")
        return

    print(f"\n👤 Name:        {profile.get('name') or '(not set)'}")
    print(f"📍 Location:    {profile.get('location') or '(not set)'}")
    print(f"📦 Public Repos: {profile.get('public_repos')}")
    print(f"👥 Followers:    {profile.get('followers')}")
    print(f"➡️  Following:    {profile.get('following')}")
    print(f"📅 Joined:       {profile.get('created_at', '')[:10]}")
    print(f"🔗 Profile URL:  {profile.get('html_url')}")

    repos = get_user_repos(username)
    if repos is None:
        return

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
    total_forks = sum(repo.get("forks_count", 0) for repo in repos)
    languages = summarize_languages(repos)

    print(f"\n⭐ Total Stars (across all repos): {total_stars}")
    print(f"🍴 Total Forks (across all repos): {total_forks}")

    print(f"\n🧑‍💻 Top Languages Used:")
    if languages:
        for lang, count in list(languages.items())[:5]:
            print(f"   {lang}: {count} repo(s)")
    else:
        print("   No language data available.")

    print(f"\n📌 Most Recently Updated Repos:")
    for repo in repos[:5]:
        stars = repo.get("stargazers_count", 0)
        print(f"   • {repo['name']}  (⭐ {stars})")


if __name__ == "__main__":
    target_username = sys.argv[1] if len(sys.argv) > 1 else "Tehseenfatima151"
    print_dashboard(target_username)
